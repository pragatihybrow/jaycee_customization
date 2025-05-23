app_name = "jaycee_customization"
app_title = "Jaycee"
app_publisher = "Pragati Dike"
app_description = "Jaycee customization app."
app_email = "pragati@mail.hybrowlabs.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "jaycee_customization",
# 		"logo": "/assets/jaycee_customization/logo.png",
# 		"title": "Jaycee",
# 		"route": "/jaycee_customization",
# 		"has_permission": "jaycee_customization.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jaycee_customization/css/jaycee_customization.css"
# app_include_js = "/assets/jaycee_customization/js/jaycee_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/jaycee_customization/css/jaycee_customization.css"
# web_include_js = "/assets/jaycee_customization/js/jaycee_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "jaycee_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"shipment" : "jaycee_customization/public/js/shipment.js"}
doctype_list_js = {"Shipment": "public/js/shipment_listview.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "jaycee_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# In your custom_app/hooks.py
# doc_events = {
#     "Shipment": {
#         "onload": "jaycee_customization.override.shipment.shipment_onload",
#         "validate": "jaycee_customization.override.shipment.shipment_validate",
#     }
# }


doctype_js = {
    "Sales Order": "public/js/sales_order.js",
    "Shipment" : "public/js/shipment.js",
    
    }


# listview_settings = {
#     "Shipment": "public/js/shipment_listview.js",
# }


override_whitelisted_methods = {
    "erpnext.stock.doctype.shipment.shipment.make_shipment": "jaycee_customization.override.sales_order.make_shipment",
    "erpnext.selling.doctype.sales_order.sales_order.make_material_request": "jaycee_customization.override.shipments.custom_make_material_request",
}


doc_events = {
    "Shipment": {
        "custom_make_material_request": "jaycee_customization.override.shipment.custom_make_material_request"
    }
}


override_doctype_dashboards = {
    "Sales Order": "jaycee_customization.override.sales_order_dashboard.get_dashboard_data",
}



# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "jaycee_customization.utils.jinja_methods",
# 	"filters": "jaycee_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "jaycee_customization.install.before_install"
# after_install = "jaycee_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "jaycee_customization.uninstall.before_uninstall"
# after_uninstall = "jaycee_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "jaycee_customization.utils.before_app_install"
# after_app_install = "jaycee_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "jaycee_customization.utils.before_app_uninstall"
# after_app_uninstall = "jaycee_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jaycee_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# override_doctype_class = {
#     "Shipment": "jaycee_customization.override.shipment.CustomShipment"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jaycee_customization.tasks.all"
# 	],
# 	"daily": [
# 		"jaycee_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"jaycee_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jaycee_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"jaycee_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "jaycee_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "jaycee_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jaycee_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["jaycee_customization.utils.before_request"]
# after_request = ["jaycee_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["jaycee_customization.utils.before_job"]
# after_job = ["jaycee_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"jaycee_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }



scheduler_events = {
    "monthly": [
        "jaycee_customization.override.scheduled_tasks.add_compensatory_leaves"
    ]
}

doc_events = {
    "Attendance": {
        "on_submit": "jaycee_customization.override.attendance.after_submit"
    }
}


# doc_events = {
#     "Attendance": {
#         "on_submit": "jaycee_customization.override.attendance.mark_comp_off"
#     }
# }
