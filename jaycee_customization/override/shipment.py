import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def custom_make_material_request(source_name, target_doc=None):

    def postprocess(source, target):
        # Setting fields on the target Shipment document
        target.delivery_customer = source.customer
        target.pickup_company = source.company
        target.custom_shipment_mode = source.custom_mode_of_transport
        target.delivery_address_name = source.customer_address
        target.pickup_address_name  = source.company_address
        target.custom_loading  = source.custom_loading
        target.custom_delivery = source.custom_delivery
        target.custom_dispatch_point  = source.custom_dispatch_point
        target.custom_discharge_point  = source.custom_discharge_point
        target.custom_testing_and_sampling = source.custom_testing_and_sampling
        target.custom_shipment_schedule  = source.custom_shipment_schedule
        target.shipment_type  = source.custom_shipment_type
        target.pickup_contact_person = source.company_contact_person
        target.delivery_contact_name = source.contact_person
        target.custom_customers_purchase_order = source.po_no
      
        sales_order_id = source.name  
        grand_total =source.grand_total
        
        target.append('custom_shipment_sales_order_', {
            'sales_order': sales_order_id,
            'grand_total' : grand_total
        })

    # Mapping the Sales Order to the Shipment document
    doc = get_mapped_doc(
        "Sales Order",
        source_name,
        {
            "Sales Order": {
                "doctype": "Shipment",
                "field_map": {
                    "name": "sales_order",
                },
                "validation": {"docstatus": ["=", 1]},
            },
        },
        target_doc,
        postprocess,
    )

    return doc

