// Daily Sales Payment Reco Form Script
// Adds Recalculate button to recalculate summary from all lines

frappe.ui.form.on('Daily Sales Payment Reco', {
    refresh: function(frm) {
        // Add Recalculate button to the page header
        if (!frm.is_new()) {
            frm.add_custom_button(__('Recalculate'), function() {
                recalculate_reco_summary(frm);
            }, __('Actions'));
            
            // Add Process QR Logs button if there are unprocessed QR logs
            check_and_add_qr_button(frm);
        }
    }
});

// Child table event handlers - must be in parent JS file to be loaded
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
    
    // Process QR button click - pass cdt and cdn for updating
    btn_container.find('.process-qr-btn').on('click', function() {
        process_line_qr_logs(frm, cdt, cdn);
    });
    
    // Recalculate button click - pass cdt and cdn for updating
    btn_container.find('.recalculate-btn').on('click', function() {
        recalculate_line_amounts(frm, cdt, cdn);
    });
}

function process_line_qr_logs(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
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
                        
                        // Update the row values in-place if line_data is returned
                        if (data.line_data) {
                            update_line_values(frm, cdt, cdn, data.line_data);
                        }
                        
                        frappe.show_alert({
                            message: __('Processed {0} QR transactions', [success_count]),
                            indicator: 'green'
                        });
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

function recalculate_line_amounts(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
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
                        // Update the row values in-place without closing the form
                        if (r.message.data) {
                            update_line_values(frm, cdt, cdn, r.message.data);
                        }
                        
                        frappe.show_alert({
                            message: __('Line amounts recalculated successfully'),
                            indicator: 'green'
                        });
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

function update_line_values(frm, cdt, cdn, data) {
    // Update each field in the row without triggering form reload
    let fields_to_update = [
        'initial_total_amount',
        'additional_amount', 
        'net_total_amount',
        'return_amount',
        'qr_amount',
        'cash_amount',
        'cheque_amount',
        'credit_amount',
        'remaining_amount',
        'settled'
    ];
    
    fields_to_update.forEach(function(field) {
        if (data.hasOwnProperty(field)) {
            frappe.model.set_value(cdt, cdn, field, data[field]);
        }
    });
    
    // Refresh the grid row to show updated values
    let grid = frm.fields_dict.daily_sales_payment_reco_line.grid;
    grid.refresh();
    
    // Re-open the form for the same row so user can see updated values
    let grid_row = grid.grid_rows_by_docname[cdn];
    if (grid_row) {
        // Small delay to let refresh complete, then re-open the form
        setTimeout(function() {
            grid_row.toggle_view(true);
        }, 100);
    }
    
    // Also reload parent document data in background to sync totals
    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: frm.doc.doctype,
            name: frm.doc.name
        },
        async: true,
        callback: function(r) {
            if (r.message) {
                // Update parent-level totals without full reload
                let parent_fields = [
                    'initial_total_amount',
                    'additional_amount',
                    'net_total_amount', 
                    'return_amount',
                    'qr_amount',
                    'cheque_amount',
                    'cash_amount',
                    'credit_amount',
                    'remaining_amount',
                    'cash_expected',
                    'cash_difference'
                ];
                
                parent_fields.forEach(function(field) {
                    if (r.message.hasOwnProperty(field)) {
                        frm.doc[field] = r.message[field];
                    }
                });
                
                frm.refresh_fields();
            }
        }
    });
}

function recalculate_reco_summary(frm) {
    frappe.confirm(
        __('This will recalculate all summary amounts from the line items. Continue?'),
        function() {
            frappe.call({
                method: 'custom_erp.api.payment_reco.recalculate_reco_summary',
                args: {
                    reco_name: frm.doc.name
                },
                freeze: true,
                freeze_message: __('Recalculating...'),
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: __('Summary recalculated successfully'),
                            indicator: 'green'
                        });
                        frm.reload_doc();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message?.message || __('Failed to recalculate'),
                            indicator: 'red'
                        });
                    }
                }
            });
        }
    );
}

function check_and_add_qr_button(frm) {
    frappe.call({
        method: 'custom_erp.api.payment_reco.get_unprocessed_qr_count_for_reco',
        args: {
            reco_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.success && r.message.data.count > 0) {
                frm.add_custom_button(
                    __('Process QR Logs ({0})', [r.message.data.count]),
                    function() {
                        process_qr_logs(frm, r.message.data);
                    },
                    __('Actions')
                );
            }
        }
    });
}

function process_qr_logs(frm, qr_data) {
    frappe.confirm(
        __('Process {0} unprocessed QR logs totaling {1}?<br><br>If QR amount exceeds initial amount, the difference will be added to Additional Amount.', 
           [qr_data.count, format_currency(qr_data.total_amount, 'NPR')]),
        function() {
            frappe.call({
                method: 'custom_erp.api.payment_reco.process_qr_logs_for_reco',
                args: {
                    reco_name: frm.doc.name
                },
                freeze: true,
                freeze_message: __('Processing QR Logs...'),
                callback: function(r) {
                    if (r.message && r.message.success) {
                        show_qr_process_results(frm, r.message.data);
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

function show_qr_process_results(frm, data) {
    let summary = data.summary || {};
    let processed = data.processed || [];
    
    let html = `
        <div style="margin-bottom: 15px;">
            <strong>Summary:</strong><br>
            Success: ${summary.success_count || 0}<br>
            Errors: ${summary.error_count || 0}<br>
            QR Applied: ${format_currency(summary.total_qr_applied || 0, 'NPR')}<br>
            Additional: ${format_currency(summary.total_additional || 0, 'NPR')}
        </div>
    `;
    
    if (processed.length > 0) {
        html += '<strong>Processed Transactions:</strong><br>';
        html += '<table class="table table-bordered" style="margin-top: 10px;">';
        html += '<thead><tr><th>Customer</th><th>QR Amount</th><th>Applied</th><th>Additional</th><th>Status</th></tr></thead>';
        html += '<tbody>';
        
        processed.forEach(function(item) {
            let status_class = item.status === 'success' ? 'text-success' : 'text-danger';
            html += `<tr>
                <td>${item.customer_name || item.customer || '-'}</td>
                <td>${format_currency(item.qr_amount || 0, 'NPR')}</td>
                <td>${format_currency(item.qr_applied || 0, 'NPR')}</td>
                <td>${format_currency(item.additional_from_qr || 0, 'NPR')}</td>
                <td class="${status_class}">${item.status}${item.error ? ': ' + item.error : ''}</td>
            </tr>`;
        });
        
        html += '</tbody></table>';
    }
    
    frappe.msgprint({
        title: __('QR Processing Complete'),
        message: html,
        indicator: 'green'
    });
    
    frm.reload_doc();
}
