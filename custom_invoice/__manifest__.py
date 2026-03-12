{
    "name": "Custom Invoice Report",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Custom PDF Invoice for account.move",
    "depends": ["account", "sale", "l10n_in", "l10n_in_sale"],
    "data": [
        "report/invoice_report.xml",
        "report/standard_invoice_inherit.xml",
        "report/standard_sale_inherit.xml",
    ],
    "installable": True,
    "application": False,
}
