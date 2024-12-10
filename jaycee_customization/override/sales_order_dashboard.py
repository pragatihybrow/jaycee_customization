from frappe import _
#connection Shipment in sales order
def get_dashboard_data(data):
    data["non_standard_fieldnames"]["Shipment"] = "sales_order"
    
   
    for transaction in data.get("transactions", []):
        if transaction.get("label") == _("Fulfillment"):
            transaction["items"].append("Shipment")
            break
    else:
        data["transactions"].append({
            "label": _("Fulfillment"),
            "items": ["Shipment"],
        })
    
    return data
