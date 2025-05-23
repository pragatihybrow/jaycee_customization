
import frappe
from frappe.model.mapper import get_mapped_doc

# Create a Shipment document from a Sales Order.
@frappe.whitelist()
def make_shipment(source_name, target_doc=None):
    # Function to set additional values on the target document after mapping.
    def set_missing_values(source, target):
        # Assign customer details based on the source Sales Order.
        target.delivery_customer = source.customer
        target.pickup_company = source.company
        target.custom_shipment_mode = source.custom_mode_of_transport
        target.delivery_address_name = source.customer_address
        target.pickup_address_name = source.company_address
        target.custom_loading = source.custom_loading
        target.custom_delivery = source.custom_delivery
        target.custom_dispatch_point = source.custom_dispatch_point
        target.custom_discharge_point = source.custom_discharge_point
        target.custom_testing_and_sampling = source.custom_testing_and_sampling
        target.custom_shipment_schedule = source.custom_shipment_schedule
        target.shipment_type = source.custom_shipment_type
        target.delivery_contact_name = source.contact_person
        target.pickup_contact_person = source.company_contact_person
        target.custom_customers_purchase_order = source.po_no

        sales_order_id = source.name  
        grand_total = source.grand_total

        # Fetch associated Sales Invoice(s)
        sales_invoices = frappe.get_all(
            'Sales Invoice',
            filters={'sales_order': sales_order_id},
            fields=['name']
        )

        # Append data to custom_shipment_sales_order_ child table
        for invoice in sales_invoices:
            target.append('custom_shipment_sales_order_', {
                'sales_order': sales_order_id,
                'grand_total': grand_total,
                'sales_invoice': invoice.name  # Add Sales Invoice number
            })

    doc = get_mapped_doc(
        "Sales Order",
        source_name,
        {
            "Sales Order": {
                "doctype": "Shipment",
                "field_map": {
                    "name": "sales_order",
                    "customer": "delivery_customer",
                },
            }
        },
        target_doc,
        set_missing_values,
    )
    return doc
