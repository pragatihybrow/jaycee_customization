import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
    # Function to set additional values on the target document after mapping
    def set_missing_values(source, target, source_parent=None):
        
        source.custom_loading = target.custom_loading
        source.delivery_company = target.company
        source.shipment_type = target.custom_shipment_type
        source.delivery_customer = target.customer
        source.custom_dispatch_point = target.custom_dispatch_point
        source.custom_discharge_point = target.custom_discharge_point
        source.custom_testing_and_sampling = target.custom_testing_and_sampling
        source.custom_shipment_schedule = target.custom_shipment_schedule
   
    # Map fields from Shipment to Sales Invoice
    doc = get_mapped_doc(
        "Shipment",  
        source_name, 
        {
            "Shipment": {  
                "doctype": "Sales Invoice",  
                "field_map": { 
                    "name": "shipment",
                    "delivery_customer": "customer", 
                    "pickup_company": "company",
                    "shipment_type": "custom_shipment_type"
                   
                },
                "postprocess": set_missing_values,  
            }
        },
        target_doc  
    )

    return doc
