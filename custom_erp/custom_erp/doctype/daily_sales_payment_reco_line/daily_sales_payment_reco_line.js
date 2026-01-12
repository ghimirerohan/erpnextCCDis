// ADDED BY AI: Daily Sales Payment Reco Line Form Script
// Adds Process QR and Recalculate buttons to line form

frappe.ui.form.on('Daily Sales Payment Reco Line', {
    form_render: function(frm, cdt, cdn) {
        // This fires when a row is opened for editing in the grid
        add_line_buttons(frm, cdt, cdn);
    }
});

function add_line_buttons(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
    // Find the grid row element
    let grid_row = frm.fields_dict.daily_sales_payment_reco_line.grid.grid_rows_by_docname[cdn];
    
    if (!grid_row || !grid_row.grid_form) return;
    
    // Remove existing custom buttons if any
    $(grid_row.grid_form.wrapper).find('.line-custom-buttons').remove();
    
    // Create button container
    let btn_container = $(`
        <div class="line-custom-buttons" style="margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px;">
            <button class="btn btn-xs btn-primary process-qr-btn" style="margin-right: 5px;">
                <i class="fa fa-qrcode"></i> Process QR
            </button>
            <button class="btn btn-xs btn-default recalculate-btn">
                <i class="fa fa-refresh"></i> Recalculate
            </button>
        </div>
    `);
    
    // Insert after the form fields
    $(grid_row.grid_form.wrapper).find('.form-group:last').after(btn_container);
    
    // Process QR button click
    btn_container.find('.process-qr-btn').on('click', function() {
        process_line_qr_logs(frm, row);
    });
    
    // Recalculate button click
    btn_container.find('.recalculate-btn').on('click', function() {
        recalculate_line_amounts(frm, row);
    });
}

function process_line_qr_logs(frm, row) {
    frappe.confirm(
        __('Process unprocessed QR logs linked to this line?<br><br>If QR amount exceeds initial amount, the difference will be added to Additional Amount.'),
        function() {
            frappe.call({
                method: 'custom_erp.api.payment_reco.process_qr_logs_for_line',
                args: {
                    line_name: row.name
                },
                freeze: true,
                freeze_message: __('Processing QR Logs...'),
                callback: function(r) {
                    if (r.message && r.message.success) {
                        let data = r.message.data;
                        let processed = data.processed || [];
                        
                        if (processed.length === 0) {
                            frappe.show_alert({
                                message: __('No unprocessed QR logs found for this line'),
                                indicator: 'blue'
                            });
                            return;
                        }
                        
                        let success_count = processed.filter(p => p.status === 'success').length;
                        
                        frappe.show_alert({
                            message: __('Processed {0} QR transactions', [success_count]),
                            indicator: 'green'
                        });
                        
                        // Reload the form to show updated values
                        frm.reload_doc();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message?.message || __('Failed to process QR logs'),
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    );
}

function recalculate_line_amounts(frm, row) {
    frappe.confirm(
        __('Recalculate amounts for this line based on Initial Total Amount?<br><br>Formula: Remaining = Net Total - QR - Cash - Cheque - Credit<br>Where: Net Total = Initial + Additional - Return'),
        function() {
            frappe.call({
                method: 'custom_erp.api.payment_reco.recalculate_line_amounts',
                args: {
                    line_name: row.name
                },
                freeze: true,
                freeze_message: __('Recalculating...'),
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: __('Line amounts recalculated successfully'),
                            indicator: 'green'
                        });
                        frm.reload_doc();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message?.message || __('Failed to recalculate. Remaining amount would be negative.'),
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    );
}

