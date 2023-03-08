from odoo import models, fields


class LinkChanged(models.Model):
    _name = 'link.changed'
    _description = 'Link Changed'

    name = fields.Char("Name")
