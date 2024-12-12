frappe.ui.form.on('Shipment', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(
                __("Sales Order"), 
                () => frm.events.get_items_from_sales_order(frm),
                __("Get Items From")
            );
        }
    },

    get_items_from_sales_order: function(frm) {
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

    validate: function(frm) {
        let sales_order_ids = frm.doc.custom_shipment_sales_order_.map(item => item.sales_order);        
        if (sales_order_ids.length > 0) {
            frappe.db.get_list('Sales Invoice', {
                filters: { 'custom_sales_order': ['in', sales_order_ids] },
                fields: ['name', 'custom_sales_order'] 
            }).then(function(sales_invoices) {                
                let sales_invoice_map = {}; 
                sales_invoices.forEach(invoice => {
                    sales_invoice_map[invoice.custom_sales_order] = invoice.name; 
                });                
                frm.doc.custom_shipment_sales_order_.forEach((item, index) => {
                    item.sales_invoice = sales_invoice_map[item.sales_order]; 
                    frm.refresh_field('custom_shipment_sales_order_');
                });
            });
        }
    }
});
