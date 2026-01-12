// ADDED BY AI: Daily Sales Payment Reco Form Script
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

