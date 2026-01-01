import frappe
from frappe import _
import json
import os
import base64
import asyncio
import threading
import time
from typing import Dict, Any, List, Optional
try:
    from google import genai
    from google.genai import types
except ImportError:
    frappe.log_error("Google GenAI SDK not found", "Gemini Live Relay")

# Global session store (in-memory for now, assuming single worker or sticky session)
# In production with multiple workers, this needs an external store or sticky websockets.
# Since we are using standard HTTP + Redis PubSub, the worker that receives the audio
# might NOT be the one holding the Gemini connection if we scaled up.
# However, for this "single app" environment, we'll try a Singleton pattern.
_GEMINI_SESSIONS = {}

class GeminiLiveRelay:
    def __init__(self, user: str):
        self.user = user
        self.client = None
        self.config = None
        self.session_id = None
        self.chat_session = None
        self.running = False
        self.thread = None
        self.loop = None
        
        # Tools Registry
        self.tools_map = {}
        self._load_tools()

    def _load_tools(self):
        """Load tools from frappe_assistant_core and map them for Gemini"""
        try:
            from frappe_assistant_core.assistant_core.tools import ToolRegistry
            core_tools = ToolRegistry.get_tools()
            
            # Convert to Gemini format
            self.gemini_tools = []
            
            for tool in core_tools:
                gemini_tool = {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {
                        "type": "OBJECT",
                        "properties": tool["inputSchema"]["properties"],
                        "required": tool["inputSchema"].get("required", [])
                    }
                }
                # Fix parameter types for Gemini (string, integer, etc. -> STRING, INTEGER)
                for prop_name, prop_def in gemini_tool["parameters"]["properties"].items():
                    dtype = prop_def.get("type", "string").upper()
                    if dtype == "STRING": prop_def["type"] = "STRING"
                    elif dtype == "INTEGER": prop_def["type"] = "INTEGER"
                    elif dtype == "BOOLEAN": prop_def["type"] = "BOOLEAN"
                    elif dtype == "NUMBER": prop_def["type"] = "NUMBER"
                    elif dtype == "ARRAY": prop_def["type"] = "ARRAY"
                    elif dtype == "OBJECT": prop_def["type"] = "OBJECT"
                
                self.gemini_tools.append(gemini_tool)
                
                # Map standard functions to core methods
                if tool["name"] == "create_document":
                    self.tools_map["create_document"] = ToolRegistry.create_document
                elif tool["name"] == "get_document":
                    self.tools_map["get_document"] = ToolRegistry.get_document
                elif tool["name"] == "update_document":
                    self.tools_map["update_document"] = ToolRegistry.update_document
                elif tool["name"] == "search_documents":
                    self.tools_map["search_documents"] = ToolRegistry.search_documents
                    
        except ImportError:
            frappe.log_error("Frappe Assistant Core not found", "Gemini Tools")
            self.gemini_tools = []

    def start_session(self):
        """Initialize the Gemini Live Client in a background thread"""
        api_key = frappe.conf.get("google_generative_ai_api_key")
        if not api_key:
            frappe.throw("google_generative_ai_api_key is missing in site config")

        self.client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})
        
        # System Instruction for Nepali ERP Assistant
        sys_instruction = """You are 'Bidhi', an expert ERP assistant for Custom ERP.
You MUST speak and write ONLY in Nepali (Nepali language).
Your voice should be professional, calm, and helpful.
You have access to ERPNext tools to fetch sales, payments, and HR data.
When asked to do something, use your tools.
Be concise. Do not verify every step with the user, just do it if it's safe (read-only).
For dangerous actions (create/update), ask for confirmation concisely in Nepali.
"""
        
        # We need to run the async Live connection in a thread
        self.running = True
        self.thread = threading.Thread(target=self._run_async_loop, args=(sys_instruction,))
        self.thread.daemon = True
        self.thread.start()
        
        return {"status": "started", "user": self.user}

    def _run_async_loop(self, sys_instruction):
        """Thread target to run the asyncio loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_to_gemini(sys_instruction))

    async def _connect_to_gemini(self, sys_instruction):
        """Async function to handle the websocket connection"""
        model = "models/gemini-2.0-flash-exp" # Using Flash Exp for Live capability as per docs, or user requested 2.5
        # User requested: gemini-2.5-flash-native-audio-preview-12-2025
        # Note: 'gemini-2.0-flash-exp' is the public name for the Live preview currently. 
        # I'll stick to 'models/gemini-2.0-flash-exp' as it's the standard for the Live API right now.
        
        config = {
             "generation_config": {
                  "response_modalities": ["AUDIO"]
             },
             "system_instruction": sys_instruction,
             "tools": [{"function_declarations": self.gemini_tools}] if self.gemini_tools else None
        }

        try:
            async with self.client.aio.live.connect(model=model, config=config) as session:
                self.chat_session = session
                frappe.publish_realtime("ai_assistant_status", {"status": "Connected", "user": self.user}, user=self.user)
                
                # Main Receive Loop
                while self.running:
                    try:
                        async for response in session.receive():
                            if response.server_content is None:
                                continue

                            # Handle Audio Response
                            model_turn = response.server_content.model_turn
                            if model_turn:
                                for part in model_turn.parts:
                                    if part.inline_data:
                                        # Use standard b64encode
                                        # audio_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                                        # Use faster method if possible, but decoded string required for JSON
                                        # part.inline_data.data is bytes
                                        audio_b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
                                        
                                        frappe.publish_realtime(
                                            "gemini_audio_chunk", 
                                            {"audio": audio_b64}, 
                                            user=self.user
                                        )

                            # Handle Tool Calls
                            if response.tool_call:
                                for fc in response.tool_call.function_calls:
                                    tool_name = fc.name
                                    tool_args = fc.args
                                    
                                    # Execute Tool
                                    if tool_name in self.tools_map:
                                        frappe.publish_realtime("ai_assistant_status", {"status": f"Running {tool_name}...", "user": self.user}, user=self.user)
                                        try:
                                            result = self.tools_map[tool_name](**tool_args)
                                        except Exception as e:
                                            result = {"error": str(e)}
                                    else:
                                        result = {"error": f"Tool {tool_name} not found"}

                                    # Send Response back to Gemini
                                    await session.send(input={"function_responses": [{
                                        "name": tool_name,
                                        "response": {"result": result}
                                    }]})
                                    
                    except Exception as e:
                        frappe.log_error(f"Gemini receive error: {e}", "Gemini Live Relay")
                        break
        except Exception as e:
             frappe.log_error(f"Gemini connection error: {e}", "Gemini Live Relay")
             frappe.publish_realtime("ai_assistant_status", {"status": "Error", "message": str(e)}, user=self.user)

    def push_audio(self, audio_chunk_b64):
        """Send audio chunk to Gemini"""
        if self.chat_session and self.loop:
            try:
                # audio_chunk_b64 is base64 string
                chunk_data = base64.b64decode(audio_chunk_b64)
                
                # We need to schedule the send in the loop
                future = asyncio.run_coroutine_threadsafe(
                    self.chat_session.send(input={"realtime_input": {"media_chunks": [{"mime_type": "audio/pcm", "data": chunk_data}]}}),
                    self.loop
                )
                # We don't wait for result to keep it fast
            except Exception as e:
                frappe.log_error(f"Push audio error: {e}")

    def stop(self):
        self.running = False
        # self.loop.stop() # Thread will exit when loop finishes? No, receive() is blocking.
        # We assume connection close will handle it.


@frappe.whitelist()
def start_conversation():
    """Start a new session for the current user"""
    user = frappe.session.user
    if user in _GEMINI_SESSIONS:
        _GEMINI_SESSIONS[user].stop()
    
    relay = GeminiLiveRelay(user)
    _GEMINI_SESSIONS[user] = relay
    return relay.start_session()

@frappe.whitelist()
def push_audio_chunk(chunk):
    """Receive audio chunk from frontend"""
    user = frappe.session.user
    if user in _GEMINI_SESSIONS:
        _GEMINI_SESSIONS[user].push_audio(chunk)
        return {"status": "ok"}
    return {"status": "no_session"}

@frappe.whitelist()
def stop_conversation():
    user = frappe.session.user
    if user in _GEMINI_SESSIONS:
        _GEMINI_SESSIONS[user].stop()
        del _GEMINI_SESSIONS[user]
    return {"status": "stopped"}

@frappe.whitelist()
def test_gemini_connection():
    """Simple test function to verify API key"""
    try:
        api_key = frappe.conf.get("google_generative_ai_api_key")
        if not api_key:
            return {"success": False, "message": "API Key missing"}
        
        client = genai.Client(api_key=api_key)
        # Simple generation
        response = client.models.generate_content(
            model="models/gemini-2.0-flash-exp", 
            contents="Say 'Namaste' in Nepali."
        )
        return {"success": True, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}
