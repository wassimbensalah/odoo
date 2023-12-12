from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate property"

    name = fields.Char('Name', required=True)

    _sql_constraints = [('type_unique', 'unique (name)', 'The property type must be unique')]
