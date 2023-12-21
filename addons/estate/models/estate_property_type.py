from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate property"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer")

    _sql_constraints = [('type_unique', 'unique (name)', 'The property type must be unique')]

    @api.depends("offer_ids")
    def _compute_offer(self):
        # This solution is quite complex. It is likely that the trainee would have done a search in a loop.
        data = self.env["estate.property.offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])
