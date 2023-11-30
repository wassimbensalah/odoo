from odoo import fields, models


class Property(models.Model):
    _name = "estate_property"
    _description = "Proprety of the estate"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Integer('Postcode')
    data_availability = fields.Date('Data Availability')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('north','North'), ('south','South'),('east','East'),('west','West')])