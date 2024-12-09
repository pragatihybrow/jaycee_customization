//add an custom button shipment under create in sales order

frappe.ui.form.on('Sales Order', {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Shipment'), function () {
                frappe.model.open_mapped_doc({
                    method: "jaycee_customization.override.sales_order.make_shipment", 
                    frm: frm,
                });
            }, __("Create"));
        }
    }
});

