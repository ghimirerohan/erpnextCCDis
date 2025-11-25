#!/usr/bin/env python3
"""Quick script to manually process a Fonepay transaction"""

import frappe
from custom_erp.custom_erp.api.fonepay import finalize_payment_from_ws

def process_transaction(tx_name):
    frappe.connect(site='development.localhost')
    frappe.set_user('Administrator')
    
    print(f"\n🔄 Processing transaction: {tx_name}")
    
    try:
        result = finalize_payment_from_ws(tx_name)
        print(f"\n✅ Result: {result}")
        
        # Reload and show transaction details
        tx = frappe.get_doc("Fonepay QR Transaction", tx_name)
        print(f"\n📊 Transaction Status:")
        print(f"   Status: {tx.status}")
        print(f"   Processed: {tx.processed}")
        print(f"   Payment Entry: {tx.payment_entry or 'Not created yet'}")
        print(f"   Amount: NPR {tx.amount}")
        print(f"   Customer: {tx.customer}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        frappe.destroy()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python test_process_payment.py <transaction_name>")
        print("Example: python test_process_payment.py g7hc50khnt")
        sys.exit(1)
    
    process_transaction(sys.argv[1])

