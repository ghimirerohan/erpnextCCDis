#!/usr/bin/env python3
"""
Diagnostic script to check Nepali Date System configuration
"""
import frappe

def diagnose():
    frappe.init(site='development.localhost')
    frappe.connect()
    
    print("\n" + "="*60)
    print("NEPALI DATE SYSTEM DIAGNOSTICS")
    print("="*60 + "\n")
    
    # Check if Custom Field exists
    print("1. Checking Custom Field...")
    field_exists = frappe.db.exists('Custom Field', {
        'dt': 'System Settings',
        'fieldname': 'enable_nepali_calendar'
    })
    
    if field_exists:
        print(f"   ✓ Custom Field exists: {field_exists}")
    else:
        print("   ✗ Custom Field NOT found!")
        print("   Run: bench migrate")
        return
    
    # Check field value
    print("\n2. Checking setting value...")
    try:
        setting_value = frappe.db.get_single_value('System Settings', 'enable_nepali_calendar')
        print(f"   Enable Nepali Calendar: {setting_value}")
        
        if not setting_value:
            print("   ⚠ Setting is DISABLED")
            print("   Go to: Setup → Settings → System Settings")
            print("   Enable: 'Enable Nepali Calendar' checkbox")
    except Exception as e:
        print(f"   ✗ Error getting value: {e}")
    
    # Check if files exist
    print("\n3. Checking files...")
    import os
    bench_path = frappe.get_site_path('..', '..', '..')
    
    files_to_check = [
        'apps/custom_erp/custom_erp/boot.py',
        'apps/custom_erp/custom_erp/public/lib/nepali.datepicker.v5.0.6.min.js',
        'apps/custom_erp/custom_erp/public/lib/sajan.nepaliFunctions.min.js',
        'apps/custom_erp/custom_erp/public/js/nepali_date_adapter.js',
        'apps/custom_erp/custom_erp/public/js/nepali_date_patch.js',
    ]
    
    all_exist = True
    for file_path in files_to_check:
        full_path = os.path.join(bench_path, file_path)
        exists = os.path.exists(full_path)
        status = "✓" if exists else "✗"
        print(f"   {status} {file_path}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n   ⚠ Some files are missing!")
        return
    
    # Check hooks
    print("\n4. Checking hooks.py configuration...")
    try:
        from custom_erp import hooks
        
        # Check app_include_js
        if hasattr(hooks, 'app_include_js'):
            nepali_js = [js for js in hooks.app_include_js if 'nepali' in js.lower()]
            print(f"   Nepali JS includes: {len(nepali_js)}")
            for js in nepali_js:
                print(f"     - {js}")
        
        # Check boot_session
        if hasattr(hooks, 'boot_session'):
            print(f"   ✓ Boot session hook: {hooks.boot_session}")
        else:
            print("   ✗ Boot session hook NOT configured!")
    
    except Exception as e:
        print(f"   ✗ Error checking hooks: {e}")
    
    # Check asset symlinks
    print("\n5. Checking asset symlinks...")
    site_path = frappe.get_site_path()
    assets_path = os.path.join(site_path, '..', 'assets', 'custom_erp')
    
    if os.path.exists(assets_path):
        js_files = os.listdir(os.path.join(assets_path, 'js')) if os.path.exists(os.path.join(assets_path, 'js')) else []
        lib_files = os.listdir(os.path.join(assets_path, 'lib')) if os.path.exists(os.path.join(assets_path, 'lib')) else []
        
        nepali_js = [f for f in js_files if 'nepali' in f.lower() and not f.endswith('.old')]
        nepali_lib = [f for f in lib_files if 'nepali' in f.lower()]
        
        print(f"   JS files with 'nepali': {len(nepali_js)}")
        for f in nepali_js:
            print(f"     - {f}")
        
        print(f"   Lib files with 'nepali': {len(nepali_lib)}")
        for f in nepali_lib:
            print(f"     - {f}")
    else:
        print("   ✗ Assets directory not found!")
        print("   Run: bench build --app custom_erp")
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS:")
    print("="*60)
    
    if not setting_value:
        print("\n1. Enable the setting:")
        print("   - Login to your ERPNext site")
        print("   - Go to: Setup → Settings → System Settings")
        print("   - Check: 'Enable Nepali Calendar'")
        print("   - Save")
    
    print("\n2. Clear browser cache:")
    print("   - Press Ctrl+Shift+R (hard refresh)")
    print("   - Or clear browser cache completely")
    
    print("\n3. Check browser console:")
    print("   - Press F12 to open Developer Tools")
    print("   - Go to Console tab")
    print("   - Look for messages starting with 'custom_erp:'")
    print("   - Look for any errors (red text)")
    
    print("\n4. Test the feature:")
    print("   - Open any document with a date field (e.g., Sales Invoice)")
    print("   - Click on the date field")
    print("   - You should see Nepali Date Picker")
    
    print("\n" + "="*60 + "\n")
    
    frappe.destroy()

if __name__ == '__main__':
    diagnose()

