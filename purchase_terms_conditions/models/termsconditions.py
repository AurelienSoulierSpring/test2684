from odoo import fields, models


class TermsConditions(models.Model):
    _name = "purchase.termsconditions"
    _description = u"Terms & Conditions"
    _order = "sequence asc"

    name = fields.Char("Name")
    sequence = fields.Integer("Sequence", default=16)
    file_ids = fields.One2many(
        "purchase.termsconditions.file", "terms_conditions_id", string="Files"
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )


class TermsConditionsFile(models.Model):
    _name = "purchase.termsconditions.file"
    _description = u"Terms & Conditions File"
    _order = "lang_id asc"

    terms_conditions_id = fields.Many2one(
        "purchase.termsconditions", string="Terms & Conditions"
    )
    pdf_file = fields.Binary("PDF file", attachment=True, required=True)
    lang_id = fields.Many2one("res.lang", string="Language", required=True)
