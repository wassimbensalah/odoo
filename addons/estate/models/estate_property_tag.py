from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag of the estate property"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [('tag_unique', 'unique (name)', 'The property tag must be unique')]
