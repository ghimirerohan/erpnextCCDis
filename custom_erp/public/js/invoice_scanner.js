frappe.ui.form.on('Purchase Invoice', {
  refresh(frm) {
    if (frm.doc.docstatus === 0) {
      frm.add_custom_button(__('Open AI Scanner'), () => {
        // Open the aiscanner app in a new window
        window.open('/aiscanner', '_blank')
      }, __('Tools'))
    }
  }
})


