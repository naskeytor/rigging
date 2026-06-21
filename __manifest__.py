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
        'base', 'contacts', 'project', 'portal'
    ],

    'post_init_hook': 'post_init_hook',

    # always loaded
    'data': [
        'views/views.xml',
        'security/rigging_groups.xml',
        'security/ir.model.access.csv',
        'security/rigging_rules.xml',

        # views / actions (todo lo que define acciones primero)
        'data/sequence.xml',

        'views/templates.xml',
        'views/rigging_dashboard_views.xml',

        'views/rigging_sizes_views.xml',
        'views/rigging_model_views.xml',
        'views/rigging_manufacturer_views.xml',

        'views/drogue_views.xml',
        'views/rigging_drogue_mount_wizard_views.xml',

        'views/rigging_lineset_views.xml',
        'views/rigging_lineset_mount_wizard_views.xml',

        'views/rigging_component_views.xml',
        'views/res_partner_views.xml',
        'views/rigging_rigging_views.xml',
        'views/rigging_tasks.xml',
        'views/rigging_task_wizard_views.xml',
        'data/rigging_task_home_data.xml',
        'views/rigging_task_home_views.xml',

        # wizards (antes de rigs si rig usa botones de wizard)
        'views/rigging_rig_jumps_wizard_views.xml',
        'views/rigging_aad_jumps_wizard_views.xml',

        # rigs al final de los modelos
        'views/rigging_rig_views.xml',

        # portal (cliente)
        'views/portal_templates.xml',

        # ✅ MENÚS SIEMPRE AL FINAL
        'views/rigging_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "assets": {
        "web.assets_backend": [
            "rigging/static/src/js/dashboard.js",
            "rigging/static/src/js/rigging_dashboard_component.js",
            "rigging/static/src/xml/rigging_dashboard.xml",
            "rigging/static/src/css/dashboard.css",

            'rigging/static/src/js/theme_switcher.js',
            'rigging/static/src/css/theme_dark.css',

            'rigging/static/src/js/rig_list_renderer.js',
            'rigging/static/src/xml/rig_list_renderer.xml',
            'rigging/static/src/css/rig_list_filters.css',
        ],
        "web.assets_frontend": [
            "rigging/static/src/css/portal_dashboard.css",
            "rigging/static/src/js/portal_dashboard.js",
        ],
    },
}
