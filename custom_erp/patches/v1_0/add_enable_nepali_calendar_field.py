"""
Patch to add 'Enable Nepali Calendar' custom field to System Settings
This creates a toggle that controls whether Nepali date UI is shown (frontend only)
"""
import frappe


def execute():
    """
    Create custom field for Nepali calendar toggle in System Settings
    """
    fieldname = 'enable_nepali_calendar'
    doctype = 'System Settings'
    
    # Check if the field already exists to avoid duplicates
    if frappe.db.exists('Custom Field', {'dt': doctype, 'fieldname': fieldname}):
        print(f"Custom field '{fieldname}' already exists in {doctype}. Skipping.")
        return
    
    try:
        # Create the custom field
        custom_field = frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': doctype,
            'label': 'Enable Nepali Calendar',
            'fieldname': fieldname,
            'fieldtype': 'Check',
            'insert_after': 'enable_onboarding',  # Place after onboarding setting
            'description': 'Toggle to enable Nepali calendar UI for all date fields (frontend only). Database stores Gregorian dates.',
            'default': '0',
            'allow_on_submit': 0,
            'depends_on': '',
            'read_only': 0,
        })
        
        custom_field.insert(ignore_permissions=True)
        frappe.db.commit()
        
        print(f"Successfully created custom field '{fieldname}' in {doctype}")
        
    except Exception as e:
        frappe.log_error(
            message=f"Failed to create custom field '{fieldname}': {str(e)}",
            title="Nepali Calendar Patch Error"
        )
        print(f"Error creating custom field: {str(e)}")
        raise

