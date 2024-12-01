# -*- coding: utf-8 -*-

{
    "name": "Contacts DND",
    "sequence": 0,
    "summary": "Contacts DND",
    "description": "Contacts DND",
    "author": "dndconsulting.com",
    "website": "dndconsulting.com",
    "category": "Uncategorized",
    "version": "1.2",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "mail",
        "utm",
        "hr",
        "contacts",
        "stock",
        "crm",
        "event"
    ],
    # always loaded
    "data": [
        # "security/security.xml",
        "security/ir.model.access.csv",
        # "data/sequence.xml",
        # "data/type_freq_data.xml",
        # "data/customer_adoption_data.xml",
        # "data/customer_category_data.xml",
        # "data/customer_interest_data.xml",
        # "data/customer_leader_data.xml",
        # "data/customer_learning_data.xml",
        # "data/customer_persona_data.xml",
        # "data/customer_posfiscale_data.xml",
        # "data/customer_potential_data.xml",
        # "data/customer_sector_data.xml",
        # "data/customer_solvency_data.xml",
        # "data/customer_function_data.xml",
        # "data/res_weekday_data.xml",
        # "data/wilaya_data.xml",
        # "data/commune_data.xml",
        # "data/locality_data.xml",
        # "data/zone_data.xml",
        "views/customer_category_views.xml",
        "views/customer_adoption_views.xml",
        "views/customer_potential_views.xml",
        "views/customer_solvency_views.xml",
        "views/customer_sector_views.xml",
        "views/customer_posfiscale_views.xml",
        "views/customer_persona_views.xml",
        "views/customer_learning_views.xml",
        "views/customer_leader_views.xml",
        "views/customer_interest_views.xml",
        "views/customer_typologie_views.xml",
        "views/customer_function_views.xml",
        "views/base_menu.xml",
        "views/wilaya_views.xml",
        "views/locality_views.xml",
        "views/commune_views.xml",
        "views/zone_views.xml",
        "views/res_partner_views.xml",
        "views/crm_lead_custom_views.xml",
        "views/event_registration.xml",
        "views/quarter_frequency.xml",
        "views/event_event.xml",
        "views/product_gamme.xml",

        #wizard
        "wizard/wizard_import_report_frequency.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # xml
            "contacts_dnd/static/src/xml/button_list.xml",
            "contacts_dnd/static/src/xml/button_kanban.xml",
            # css
            "contacts_dnd/static/src/css/commune.css",
            # js
            "contacts_dnd/static/src/js/tree_button.js"
        ],
    },
    "application": True,
    "license": "LGPL-3",
}  # type: ignore
