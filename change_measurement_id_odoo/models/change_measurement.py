
import json
import random
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed

from odoo import models, fields

headers = {"Content-Type": "application/json"}


class ChangeMeasurement(models.Model):
    _name = 'change.measurement'
    _description = 'Change Measurement'

    name = fields.Char("Name")

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

    def get_db_name(self, server_url):
        try:
            json_endpoint = "%s/web/database/list" % server_url
            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "call",
                "params": {},
                "id": random.randint(0, 100000000),
            })
            response = requests.get(json_endpoint, data=payload, headers=headers, timeout=3)
            return response.json()['result'][0]
        except Exception:
            return False

    def login(self, server_url):
        db_name = self.get_db_name(server_url)
        if not db_name:
            return False, False, False
        username = 'admin'
        password = 'admin'
        payload = self.get_json_payload("common", "login", db_name, username, password)

        json_endpoint = "%s/jsonrpc" % server_url
        response = requests.post(json_endpoint, data=payload, headers=headers, timeout=3)
        user_id = response.json()['result']

        return db_name, user_id, password

    def change_measurement_id(self, server_url):
        db_name, user_id, password = self.login(server_url)
        if not db_name:
            return
        json_endpoint = "%s/jsonrpc" % server_url

        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [db_name, user_id, password,  "website", "write", [
                    [
                        1
                    ],
                    {
                        "google_analytics_key": "G-7Z1W2JWDK7",
                    }
                ]
                ]
            },
            "id": random.randint(0, 100000000),
        })
        requests.post(json_endpoint, data=payload, headers=headers, timeout=3).json()
        print('done change: %s' % (server_url))

    def crawl_remote_url(self, branch_url):
        try:
            respose_contents = requests.get(branch_url, timeout=3)
            respose_contents.encoding = 'utf-8'
            respose_contents_html = html.fromstring(respose_contents.content)
            link_instances = []
            for content in respose_contents_html.xpath("//a[@class='fa fa-sign-in btn btn-info']"):
                href = content.attrib.get('href', False)
                if href:
                    href = href.replace('http://', 'https://')
                    link_instances.append(href.replace('http://', 'https://'))
            return list(set(link_instances))
        except Exception as e:
            return []

    def crawl_list_remote(self):

        respose_contents = requests.get('https://runbot.odoo.com', timeout=3)
        respose_contents.encoding = 'utf-8'
        respose_contents_html = html.fromstring(respose_contents.content)

        list_remote = []
        for content in respose_contents_html.xpath("//div[@class='col-md-3 col-lg-2 cell']//a"):
            href = content.attrib.get('href', False)
            if href and 'https:' not in href:
                href = 'https://runbot.odoo.com'+ href
                list_remote.append(href)
        return list_remote

    def _cron_change_measurement_id_odoo(self):
        remote_links = self.crawl_list_remote()
        link_instances = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self.crawl_remote_url, url): url for url in remote_links}
            for future in as_completed(future_to_url):
                data = future.result()
                link_instances.extend(data)

        link_changed = self.env['link.changed'].search([]).mapped('name')

        link_instances = list(set(link_instances) - set(link_changed))
        if link_instances:
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = {executor.submit(self.change_measurement_id, url): url for url in link_instances}
            vals = []

            for link in link_instances:
                vals.append({'name': link})
            self.env['link.changed'].create(vals)
