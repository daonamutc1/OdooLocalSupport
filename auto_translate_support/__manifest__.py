{
    'name': "Translate support",
    'name_vi_VN': "Hỗ trợ dịch",

    'summary': '',

    'summary_vi_VN': '',

    'description': """
What it does
============


    """,
    'version': '0.1',
    'depends': ['viin_website_auto_translation_google'],
    'data': [
        "security/ir.model.access.csv",
        # "data/data.xml"
    ],
    'demo': [
        'data/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
