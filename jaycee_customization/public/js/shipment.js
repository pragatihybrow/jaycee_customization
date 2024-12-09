

frappe.ui.form.on('Shipment', {
    refresh: function (frm) {
        // Add the "Get Items " button for draft documents
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(
                __("Sales Order"), 
                () => frm.events.get_items_from_sales_order(frm),
                __("Get Items From") 
            );
        }
    },

    get_items_from_sales_order: function (frm) {
        erpnext.utils.map_current_doc({
            method: "jaycee_customization.override.shipment.custom_make_material_request",
            source_doctype: "Sales Order",  
            target: frm,  
            setters: {
                customer: frm.doc.customer || undefined,  
                delivery_date: undefined, 
            },
            get_query_filters: {
                docstatus: 1,  
                status: ["not in", ["Closed", "On Hold"]],  
                per_delivered: ["<", 99.99], 
                company: frm.doc.company,  
            },
        });
    },
});

