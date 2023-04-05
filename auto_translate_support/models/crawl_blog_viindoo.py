from psycopg2 import sql
import json
import random
import requests
from lxml import html

from odoo import fields, models, api, _


server_url = 'https://viindoo.com'
# db_name = 'dd5f257t1ouu'
db_name = 'i2l3lurxd24s'
username = 'daonamutc@gmail.com'
password = 'Namkim92@'
headers = {"Content-Type": "application/json"}
json_endpoint = "%s/jsonrpc" % server_url
user_id = None


class CrawlBlogViindoo(models.Model):
    _name = 'crawl.blog.viindoo'
    _description = 'Crawl blog viindoo'

    def get_json_payload(self, service, method, *args):
        return json.dumps({
            "jsonrpc": "2.0",
            "method": 'call',
            "params": {
                "service": service,
                "method": method,
                "args": args
            },
            "id": random.randint(0, 100000000),
        })

    def _login_viindoo(self):
        payload = self.get_json_payload("common", "login", db_name, username, password)
        response = requests.post(json_endpoint, data=payload, headers=headers)
        user_id = response.json()['result']
        return user_id

    def _crawl_blog_viindoo(self):
        user_id = self._login_viindoo()
        if not user_id:
            return
        model_name = 'blog.post'
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [db_name, user_id, password,  model_name, "search_read", [], {
                    "domain": [
                    ],
                }],
            },
            "id": random.randint(0, 100000000),
        })
        response = requests.post(json_endpoint, data=payload, headers=headers).json()
        vals = []
        for res in response.get('result'):
            val = {
                'id': res.get('id'),
                'name': res.get('name'),
            }
            vals.append(val)
        self._create_muilple(vals)

    def _create_muilple(self, vals_list):
        if not vals_list:
            return
        fields_name = list(vals_list[0].keys())
        vals = []
        for val in vals_list:
            vals.append(tuple([val[f] for f in fields_name]))
        query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
            sql.Identifier('blog_post'),
            sql.SQL(", ").join(sql.Identifier(name) for name in fields_name),
            sql.SQL(", ".join([str(row).replace('None', 'Null') for row in vals])),
        )
        self.env.cr.execute(query)
