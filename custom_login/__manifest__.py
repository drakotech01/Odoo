{
    'name': 'Custom Login Page',
    'version': '18.0.1.0',
    'summary': 'Customize the Odoo 18 login page',
    'author': 'Your Name',
    'website': 'Your Website',
    'category': 'Themes/Backend',
    'depends': ['web'],   
    'assets': {
        'web.assets_backend': [
            'custom_login/static/src/css/login.css',
            'custom_login/static/src/xml/login_template.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}