from odoo import fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the estate property"

    price = fields.Float("Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)