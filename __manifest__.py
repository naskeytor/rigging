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
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/rigging_dashboard_views.xml',

        'views/rigging_sizes_views.xml',
        'views/rigging_model_views.xml',
        'views/rigging_manufacturer_views.xml',
        'views/drogue_views.xml',
        'views/rigging_drogue_mount_wizard_views.xml',
        'views/rigging_component_views.xml',
        'views/rigging_rigging_views.xml',
        'views/rigging_lineset_views.xml',
        'views/rigging_lineset_mount_wizard_views.xml',
        'views/rigging_menus.xml',

        # 👇 PRIMERO el wizard (define la acción)
        'views/rigging_rig_jumps_wizard_views.xml',

        # 👇 DESPUÉS la vista del rig que usa el botón
        'views/rigging_rig_views.xml',

        'views/rigging_aad_jumps_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "assets": {
        "web.assets_backend": [
            "rigging/static/src/js/dashboard.js",
            "rigging/static/src/css/dashboard.css",

            'rigging/static/src/js/theme_switcher.js',
            'rigging/static/src/css/theme_dark.css',
        ],
    },
}
