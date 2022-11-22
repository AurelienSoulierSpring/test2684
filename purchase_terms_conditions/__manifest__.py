{
    "name": "PDF purchase terms and conditions ",
    "summary": """
        Merge "terms & conditions" pdf file to purchase pdf.""",
    "author": "Scopea",
    "website": "http://scopea.fr",
    "category": "Purchase",
    "version": "15.0.1.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["purchase"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/purchase.xml",
        "views/termsconditions.xml",
    ],
}
