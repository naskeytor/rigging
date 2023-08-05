# -*- coding: utf-8 -*-
{
    'name': "Rigging",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

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
        'views/rigging_manifacturer_view.xml',
        'views/rigging_model_view.xml',
        'views/rigging_status_view.xml',
        'views/rigging_type_view.xml',
        'views/rigging_container_view.xml',
        'views/rigging_canopy_view.xml',
        'views/rigging_reserve_view.xml',
        'views/rigging_aad_view.xml',
        'views/rigging_rigs_view.xml',
        'views/rigging_rigging_view.xml',
        'views/rigging_canopy_size_view.xml',
        'views/rigging_container_size_view.xml',
        'views/rigging_components_view.xml',
        'views/rigging_serial_view.xml',
        'views/rigging_comp_view.xml',
        'views/rigging_compt_view.xml',
        'views/rigging_menus.xml',
        'views/rigging_input_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
