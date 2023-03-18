{
    'name': "Marketing Keyword Planner Support",
    'name_vi_VN': "Lập Kế Hoạch Từ Khóa Marketing Support",

    'summary': 'Marketing Keyword Planner System',

    'summary_vi_VN': 'Bộ công cụ lập Kế hoạch Từ khóa Marketing',

    'description': """
What it does
============
This module is used for keyword planning:


    """,

    'author': "Viindoo",
    'website': "https://viindoo.com/apps/app/15.0/viin_mkp",
    'live_test_url': "https://v15demo-int.viindoo.com",
    'live_test_url_vi_VN': "https://v15demo-vn.viindoo.com",
    'support': "apps.support@viindoo.com",
    'sequence': 27,
    'category': 'Marketing',
    'version': '0.1',
    'depends': ['viin_mkp_google_site_kit'],
    'data': [
        # "data/marketing.keyword.csv",
        # "data/marketing.keyword.ads.historical.metrics.csv"
    ],
    'demo': [
        # 'data/demo.xml',
        'data/res.country.csv',
    ],
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
