import codecs
from io import BytesIO

from odoo import fields, models
from PyPDF2 import PdfFileMerger, PdfFileReader


class MergeReport(models.Model):
    _inherit = "ir.actions.report"

    apply_t_and_c = fields.Boolean("Merge T&C (sale.order only)")

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        # add T&C by merging pdfs
        if self.apply_t_and_c:
            pdf_content = self._merge_pdfs_tc(pdf_content, res_ids)
        return super(MergeReport, self)._post_pdf(
            save_in_attachment, pdf_content, res_ids
        )

    def _merge_pdfs_tc(self, pdf, docids):
        sale_order_id = self.env["sale.order"].browse(docids[0])
        extra_pdfs = self._get_extra_pdf(sale_order_id)
        merger = PdfFileMerger()
        merger.append(PdfFileReader(BytesIO(pdf)), import_bookmarks=False)
        for p in extra_pdfs:
            pdf_reader = PdfFileReader(BytesIO(p))
            merger.append(pdf_reader, import_bookmarks=False)
        output_buffer = BytesIO()
        merger.write(output_buffer)
        pdf = output_buffer.getvalue()
        return pdf

    def _get_extra_pdf(self, sale_order_id):
        extra_pdfs = []
        if sale_order_id.terms_conditions_id:
            terms = sale_order_id.terms_conditions_id
            file_desc = terms.file_ids.filtered(
                lambda f: f.lang_id.code == sale_order_id.partner_id.lang
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
