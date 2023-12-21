from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of the estate"
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    postcode = fields.Integer('Postcode')
    data_availability = fields.Date('Data Availability', copy=False,
                                    default=fields.Date.add(fields.Date.today(), month=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], string="State", default='new', required=True, copy=False)
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_determine_best_price_offer")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must have a positive value"),
        ("check_selling_price", "CHECK(selling_price > 0)", "The selling price must have a positive value"), ]

    def action_set_property_as_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("A canceled property can't be set as sold")
            record.state = "sold"
        return True

    def action_set_property_as_canceled(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property can't be set as canceled")
            record.state = "canceled"
        return True

    @api.depends("living_area", "garden_area", "offer_ids")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _determine_best_price_offer(self):
        for record in self:
            price = 0
            for offer in record.offer_ids:
                if offer.price > price:
                    price = offer.price
            record.best_price = price

    @api.onchange("garden")
    def _onchange(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, 0.0, precision_digits=2) == 0 :
                continue

            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise exceptions.ValidationError("The selling price should not be lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def unlink_property(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise exceptions.UserError("Only new and canceled properties can be deleted.")

