from odoo import fields, models


class MergePurchase(models.Model):
    _inherit = "purchase.order"

    s_terms_conditions_id = fields.Many2one(
        "purchase.termsconditions", string="Terms & Conditions"
    )
