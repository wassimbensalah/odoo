from odoo import fields, models


class Property(models.Model):
    _name = "estate_property"
    _description = "Property of the estate"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
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
        [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default='new', required=True, copy=False)
