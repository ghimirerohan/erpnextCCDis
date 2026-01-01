<template>
  <div class="h-screen w-screen flex flex-col bg-slate-900 text-white overflow-hidden">
    <!-- Header -->
    <header class="p-4 flex items-center justify-between border-b border-white/10 bg-slate-800/50 backdrop-blur-md">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
          <FeatherIcon name="mic" class="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 class="text-lg font-bold">विधि (Bidhi)</h1>
          <p class="text-xs text-slate-400">AI ERP Assistant</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-white/5">
          <div class="w-2 h-2 rounded-full" :class="connectionStatusColor"></div>
          <span class="text-xs font-medium">{{ connectionStatus }}</span>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 relative flex flex-col items-center justify-center p-6">
      
      <!-- Orb Visualizer -->
      <div class="relative w-64 h-64 mb-12 flex items-center justify-center">
        <!-- Glow effect -->
        <div class="absolute inset-0 bg-indigo-500/20 blur-3xl rounded-full" :class="{ 'animate-pulse': isAssistantSpeaking }"></div>
        
        <!-- Main Orb -->
        <div 
          class="relative w-48 h-48 rounded-full bg-gradient-to-br from-indigo-600 to-purple-700 shadow-2xl flex items-center justify-center transition-all duration-300"
          :class="{ 'scale-110': isAssistantSpeaking, 'scale-95': isUserSpeaking }"
        >
          <!-- Inner ripples -->
          <div class="absolute inset-0 rounded-full border border-white/10 animate-ping opacity-20" v-if="state === 'listening'"></div>
          <div class="absolute inset-0 rounded-full border border-white/10 animate-ping delay-100 opacity-10" v-if="state === 'listening'"></div>
          
          <FeatherIcon 
            :name="stateIcon" 
            class="w-16 h-16 text-white/90 drop-shadow-lg transition-all duration-300" 
            :class="{ 'animate-bounce': state === 'processing' }"
          />
        </div>
      </div>

      <!-- Status Text -->
      <div class="text-center space-y-2 max-w-md mx-auto z-10">
        <h2 class="text-2xl font-bold tracking-tight min-h-[2rem]">
            {{ mainStatusText }}
        </h2>
        <p class="text-slate-400 text-sm min-h-[1.5rem]">
            {{ subStatusText }}
        </p>
      </div>

      <!-- Controls -->
      <div class="mt-12 flex items-center gap-6 z-10">
        <Button 
          v-if="state === 'idle'"
          variant="solid" 
          theme="indigo" 
          size="lg" 
          class="rounded-full px-8 shadow-xl shadow-indigo-500/20 hover:scale-105 transition-transform"
          @click="startConversation"
        >
          <div class="flex items-center gap-2">
            <FeatherIcon name="mic" class="w-5 h-5" />
            <span>Start Conversation</span>
          </div>
        </Button>

        <Button 
          v-else
          variant="solid" 
          theme="red" 
          size="lg" 
          class="rounded-full px-8 shadow-xl shadow-red-500/20 hover:scale-105 transition-transform"
          @click="stopConversation"
        >
           <div class="flex items-center gap-2">
            <FeatherIcon name="square" class="w-5 h-5" />
            <span>End Session</span>
          </div>
        </Button>
      </div>

    </main>

    <!-- Logs Drawer (Collapsible) -->
    <div 
        class="bg-slate-800/80 backdrop-blur border-t border-white/5 transition-all duration-300 ease-in-out flex flex-col"
        :class="showLogs ? 'h-64' : 'h-10'"
    >
        <div 
            class="h-10 flex items-center justify-between px-4 cursor-pointer hover:bg-white/5"
            @click="showLogs = !showLogs"
        >
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Live Logs</span>
            <FeatherIcon :name="showLogs ? 'chevron-down' : 'chevron-up'" class="w-4 h-4 text-slate-500" />
        </div>
        <div class="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs" ref="logsContainer">
            <div v-for="(log, i) in logs" :key="i" class="flex gap-2">
                <span class="text-slate-500">[{{ log.time }}]</span>
                <span :class="log.color">{{ log.message }}</span>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, getCurrentInstance } from 'vue'
import { Button, FeatherIcon, call } from 'frappe-ui'
import { useSocket } from '../../shared/socket'

// State
const state = ref('idle') // idle, connecting, listening, processing, speaking
const isUserSpeaking = ref(false)
const isAssistantSpeaking = ref(false)
const connectionStatus = ref('Disconnected')
const logs = ref([])
const showLogs = ref(false)

// Audio Contexts
let audioContext = null
let mediaStream = null
let workletNode = null
let nextStartTime = 0

// Socket reference
let socket = null

// Constants
const INPUT_SAMPLE_RATE = 16000
const OUTPUT_SAMPLE_RATE = 24000

// Computed
const connectionStatusColor = computed(() => {
    switch(connectionStatus.value) {
        case 'Connected': return 'bg-green-500'
        case 'Connecting...': return 'bg-yellow-500'
        case 'Error': return 'bg-red-500'
        default: return 'bg-slate-500'
    }
})

const stateIcon = computed(() => {
    switch(state.value) {
        case 'listening': return 'mic'
        case 'speaking': return 'volume-2'
        case 'processing': return 'cpu'
        case 'connecting': return 'loader'
        case 'idle': return 'power'
        default: return 'mic-off'
    }
})

const mainStatusText = computed(() => {
    switch(state.value) {
        case 'listening': return 'सुन्दैछु... (Listening)'
        case 'speaking': return 'बोल्दैछु... (Speaking)'
        case 'processing': return 'सोच्दैछु... (Thinking)'
        case 'connecting': return 'जडान गर्दै... (Connecting)'
        case 'idle': return 'नमस्ते! सुरु गर्न बटन थिच्नुहोस्'
        default: return 'Ready'
    }
})

const subStatusText = computed(() => {
    if (state.value === 'idle') return 'Press Start to talk to ERPNext'
    return 'Voice Mode Active'
})

// Logger
function log(msg, type='info') {
    const time = new Date().toLocaleTimeString().split(' ')[0]
    let color = 'text-slate-300'
    if (type === 'error') color = 'text-red-400'
    if (type === 'success') color = 'text-green-400'
    if (type === 'warning') color = 'text-yellow-400'
    
    logs.value.push({ time, message: msg, color })
    nextTick(() => {
        const container = document.querySelector('.overflow-y-auto')
        if (container) container.scrollTop = container.scrollHeight
    })
}

// --- Audio Handling ---

// 1. Audio Capture (Worklet Code)
const workletCode = `
class RecorderProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.bufferSize = 4096; // Adjust chunk size
        this.buffer = new Float32Array(this.bufferSize);
        this.index = 0;
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            const channelData = input[0];
            for (let i = 0; i < channelData.length; i++) {
                this.buffer[this.index++] = channelData[i];
                if (this.index >= this.bufferSize) {
                    this.port.postMessage(this.buffer);
                    this.index = 0;
                }
            }
        }
        return true;
    }
}
registerProcessor('recorder-processor', RecorderProcessor);
`;

async function initAudioContext() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: INPUT_SAMPLE_RATE // Try to request 16kHz context directly
        });
        
        // Load Worklet
        const blob = new Blob([workletCode], { type: 'application/javascript' });
        const url = URL.createObjectURL(blob);
        await audioContext.audioWorklet.addModule(url);
        
        log('Audio engine initialized', 'success')
    } catch (e) {
        log('Audio init failed: ' + e.message, 'error')
    }
}

async function startMicrophone() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                channelCount: 1,
                sampleRate: INPUT_SAMPLE_RATE,
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            } 
        });
        
        const source = audioContext.createMediaStreamSource(mediaStream);
        workletNode = new AudioWorkletNode(audioContext, 'recorder-processor');
        
        workletNode.port.onmessage = (event) => {
            const float32Array = event.data;
            sendAudioChunk(float32Array);
        };
        
        source.connect(workletNode);
        // Don't connect to destination to avoid feedback
        
        state.value = 'listening'
        isUserSpeaking.value = true
        log('Microphone active', 'success')
    } catch (e) {
        log('Mic access denied: ' + e.message, 'error')
        state.value = 'idle'
    }
}

function stopMicrophone() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    if (workletNode) {
        workletNode.disconnect();
        workletNode = null;
    }
    isUserSpeaking.value = false;
}

// 2. Audio Sending
function floatTo16BitPCM(float32Array) {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    for (let i = 0; i < float32Array.length; i++) {
        let s = Math.max(-1, Math.min(1, float32Array[i]));
        s = s < 0 ? s * 0x8000 : s * 0x7FFF;
        view.setInt16(i * 2, s, true); // Little endian
    }
    return buffer;
}

function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

const sendAudioChunk = async (float32Array) => {
    if (state.value !== 'listening' && state.value !== 'speaking' && state.value !== 'processing') return;
    
    // Convert to PCM16
    const pcmBuffer = floatTo16BitPCM(float32Array);
    const base64Audio = arrayBufferToBase64(pcmBuffer);
    
    // Send to backend via frappe-ui call (fire and forget)
    try {
        call('custom_erp.api.live_relay.push_audio_chunk', { chunk: base64Audio }).catch(() => {});
    } catch (e) {
        // Ignore drop
    }
}


// 3. Audio Playback
function handleIncomingAudio(base64Data) {
    // Decode Base64 to ArrayBuffer
    const binaryString = window.atob(base64Data);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    
    // PCM 16bit to Float32
    const int16 = new Int16Array(bytes.buffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
        float32[i] = int16[i] / 32768.0;
    }
    
    // Queue for playback
    queueAudio(float32);
}

function queueAudio(float32Array) {
    if (!audioContext) return;
    
    // Create buffer
    const buffer = audioContext.createBuffer(1, float32Array.length, OUTPUT_SAMPLE_RATE);
    buffer.getChannelData(0).set(float32Array);
    
    const source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(audioContext.destination);
    
    // Schedule
    const currentTime = audioContext.currentTime;
    if (nextStartTime < currentTime) {
        nextStartTime = currentTime;
    }
    
    source.start(nextStartTime);
    nextStartTime += buffer.duration;
    
    // UI state
    isAssistantSpeaking.value = true;
    state.value = 'speaking';
    
    source.onended = () => {
        if (Math.abs(nextStartTime - audioContext.currentTime) < 0.1) {
            isAssistantSpeaking.value = false;
            state.value = 'listening'; // Back to listening
        }
    };
}


// --- App Logic ---

async function startConversation() {
    connectionStatus.value = 'Connecting...';
    state.value = 'connecting';
    
    try {
        await initAudioContext();
        
        // Call backend to start using frappe-ui's call
        const res = await call('custom_erp.api.live_relay.start_conversation');
        log('Session started: ' + (res?.status || 'OK'), 'success');
        
        connectionStatus.value = 'Connected';
        await startMicrophone();
        
    } catch (e) {
        connectionStatus.value = 'Error';
        state.value = 'idle';
        log(e.message || 'Connection failed', 'error');
    }
}

async function stopConversation() {
    stopMicrophone();
    state.value = 'idle';
    connectionStatus.value = 'Disconnected';
    
    try {
        await call('custom_erp.api.live_relay.stop_conversation');
        log('Session stopped', 'warning');
    } catch (e) {
        log(e.message || 'Error stopping', 'error');
    }
}

// Socket Listeners
onMounted(() => {
    // Get socket from global or instance
    socket = useSocket() || window.$socket
    
    if (socket) {
        socket.on('gemini_audio_chunk', (data) => {
            if (data && data.audio) {
                handleIncomingAudio(data.audio);
            }
        });
        
        socket.on('ai_assistant_status', (data) => {
            log(`Backend: ${data?.status || 'update'} ${data?.message || ''}`, 'info');
            if (data?.status?.includes('Running')) {
                state.value = 'processing';
            }
        });
    }

    log('Bidhi Assistant Ready', 'info');
})

onUnmounted(() => {
    stopConversation();
    if (socket) {
        socket.off('gemini_audio_chunk');
        socket.off('ai_assistant_status');
    }
    if (audioContext) audioContext.close();
})

</script>
