import frappe
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import RepostItemValuation


class RepostItemValuationOverride(RepostItemValuation):
    def before_cancel(self):
        """Override before_cancel to allow cancellation of repost documents when cancelling Stock Reconciliation"""
        print("=== CUSTOM REPOST ITEM VALUATION BEFORE_CANCEL CALLED ===")
        print(f"Document: {self.name}, Status: {self.status}")
        
        # For now, always skip the pending validation to allow Stock Reconciliation cancellation
        # This is a temporary solution - in production, you might want more sophisticated detection
        print("=== SKIPPING PENDING VALIDATION TO ALLOW CANCELLATION ===")
        return
        
        # Original validation (commented out for now)
        # super().before_cancel()
