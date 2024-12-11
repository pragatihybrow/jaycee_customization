frappe.listview_settings['Shipment'] = {
   formatters: {
        custom_shipment_status(val) {
            if (val=="Planned"){
              return "<span class='indicator-pill orange'>"+__(val)+"</span>"
          }
              if (val=="Booked"){
                return "<span class='indicator-pill yellow'>"+__(val)+"</span>"
                }
                if (val=="Gate In"){
                  return "<span class='indicator-pill blue'>"+__(val)+"</span>"
                  }
                  if (val=="Sailed"){
                    return "<span class='indicator-pill red'>"+__(val)+"</span>"
                    }
                    if (val=="Discharge"){
                      return "<span class='indicator-pill green'>"+__(val)+"</span>"
                      }
                      else{
                        return "<span class='indicator-pill purple'>"+__(val)+"</span>"
                      }
          }
    }


}