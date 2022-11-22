from odoo import fields, models


class MergeSaleOrder(models.Model):
    _inherit = "sale.order"

    terms_conditions_id = fields.Many2one(
        "sale.termsconditions", string="Terms & Conditions"
    )
