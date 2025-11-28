{
    'name': "rigging",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        "views/rigging_menus.xml",
        "views/rigging_sizes_views.xml",
        "views/rigging_model_views.xml",
        "views/rigging_manufacturer_views.xml",
        "views/rigging_rigging_views.xml",
        "views/rigging_component_views.xml",
        "views/rigging_rig_views.xml",
        'views/rigging_aad_jumps_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
