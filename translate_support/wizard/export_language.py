# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import contextlib
import io
import csv
import re

from odoo import api, fields, models, tools, _


NEW_LANG_KEY = '__new__'


class ExportLanguages(models.TransientModel):
    _name = "export.language"
    _description = 'Export Language'

    name = fields.Char('File Name', readonly=True)
    lang_id = fields.Many2one('res.lang', string='Language', required=True,
                              default=lambda self: self.env.ref('base.lang_vi_VN'))
    module_id = fields.Many2one('ir.module.module', string='Apps To Export', domain=[('state', '=', 'installed')])

    def act_getfile(self):
        self.ensure_one()
        this = self[0]
        lang = this.lang_id

        mods = [this.module_id.name]

        with contextlib.closing(io.BytesIO()) as buf:
            tools.trans_export(NEW_LANG_KEY, [this.module_id.name], buf, 'po', self._cr)
            out_pot = base64.encodebytes(buf.getvalue())

            tools.trans_export(lang.name, [this.module_id.name], buf, 'po', self._cr)
            out_po = base64.encodebytes(buf.getvalue())

        filename_pot = "%s.%s" % (this.module_id.name, 'pot')
        filename_po = "%s.%s" % (lang.code, 'po')

        data_pot = out_pot.decode('utf-8').splitlines()
        data_po = out_pot.decode('utf-8').splitlines()
        # Open the file for writing
        with open("tmp.csv", "w") as csv_file:
            # Create the writer object with tab delimiter
            writer = csv.writer(csv_file, delimiter = '\t')
            for line in data_pot:
                # Writerow() needs a list of data to be written, so split at all empty spaces in the line 
                writer.writerow(re.split('\s+',line))
