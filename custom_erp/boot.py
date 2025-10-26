"""
Boot session hook to add custom_erp settings to frappe.boot
This allows client-side code to access settings without async DB calls
"""
import frappe


def get_boot_settings(boot):
    """
    Add enable_nepali_calendar setting to frappe.boot for immediate client-side access
    
    Args:
        boot (dict): The boot dictionary that gets sent to the client
    """
    try:
        # Get the Nepali calendar setting from System Settings
        enable_nepali_calendar = frappe.db.get_single_value(
            'System Settings', 
            'enable_nepali_calendar'
        )
        
        # Add to boot dictionary (defaults to False if not set)
        boot['enable_nepali_calendar'] = enable_nepali_calendar or False
        
    except Exception as e:
        # Fail gracefully - field might not exist yet before migration
        frappe.log_error(
            message=f"Failed to load enable_nepali_calendar setting: {str(e)}",
            title="Boot Hook Error"
        )
        boot['enable_nepali_calendar'] = False

