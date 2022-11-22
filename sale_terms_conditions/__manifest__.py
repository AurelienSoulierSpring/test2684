{
    "name": "PDF terms and conditions ",
    "summary": """
        Merge "terms & conditions" pdf file to quotation pdf.""",
    "description": """
        This module allow to upload terms and conditions as
        PDF file what will be merged at the end of the sale report
        (e.g. Quotation)""",
    "author": "Scopea",
    "website": "http://scopea.fr",
    "category": "Sale",
    "version": "15.0.1.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["sale_management", "base"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/sale.xml",
        "views/termsconditions.xml",
        "views/report.xml",
    ],
}
