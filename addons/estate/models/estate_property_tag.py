from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag of the estate property"

    name = fields.Char("Name", required=True)

    _sql_constraints = [('tag_unique', 'unique (name)', 'The property tag must be unique')]
