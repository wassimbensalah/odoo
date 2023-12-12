from odoo import api, fields, models, exceptions
from datetime import datetime



class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the estate property"

    price = fields.Float("Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The price offer must have a positive value')
    ]

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "sold":
                raise exceptions.UserError("This property is already sold")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "sold"
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
    @api.depends("create_date", "validity", "date_deadline")
    def _compute_deadline(self):
        for record in self:
            fallback_date = record.create_date or fields.Datetime.today()
            record.date_deadline = fields.Date.add(fallback_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            fmt = '%Y-%m-%d'
            d1 = datetime.strptime(fields.Date.to_string(record.create_date), fmt)
            d2 = datetime.strptime(fields.Date.to_string(record.date_deadline), fmt)
            print("d2: ", d2)
            print("d1: ", d1)
            date_difference = (d2 - d1).days
            print("date_difference: ", date_difference)
            record.validity = date_difference

