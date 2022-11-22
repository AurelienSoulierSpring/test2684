import codecs
from io import BytesIO

from odoo import api, models
from PyPDF2 import PdfFileMerger, PdfFileReader


class MergeReport(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def render_qweb_pdf(self, res_ids=None, data=None):
        # add T&C by merging pdfs
        pdf, x = super(MergeReport, self).render_qweb_pdf(res_ids, data)
        if self.report_name in [
            "purchase.report_purchaseorder",
            "purchase.report_purchasequotation",
        ]:
            pdf = self._purchase_merge_pdfs(pdf, res_ids)
        return pdf, "pdf"

    def _purchase_merge_pdfs(self, pdf, docids):
        purchase_order_id = self.env["purchase.order"].browse(docids[0])
        extra_pdfs = self._purchase_get_extra_pdf(purchase_order_id)
        merger = PdfFileMerger()
        merger.append(PdfFileReader(BytesIO(pdf)), import_bookmarks=False)
        for p in extra_pdfs:
            pdf_reader = PdfFileReader(BytesIO(p))
            merger.append(pdf_reader, import_bookmarks=False)
        output_buffer = BytesIO()
        merger.write(output_buffer)
        pdf = output_buffer.getvalue()
        return pdf

    def _purchase_get_extra_pdf(self, purchase_order_id):
        extra_pdfs = []
        if purchase_order_id.s_terms_conditions_id:
            terms = purchase_order_id.s_terms_conditions_id
            file_desc = terms.file_ids.filtered(
                lambda f: f.lang_id.code == purchase_order_id.partner_id.lang
            )
            if not file_desc:
                file_desc = terms.file_ids.filtered(
                    lambda f: f.lang_id.iso_code == "en"
                )
            if not file_desc:
                file_desc = terms.file_ids
            file_desc = file_desc and file_desc[0]

            if file_desc:
                pdf = codecs.decode(file_desc.pdf_file, "base64")
                extra_pdfs.append(pdf)

        return extra_pdfs
