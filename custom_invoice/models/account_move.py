from odoo import models, fields, api

DEFAULT_BANK_NOTE = """<p><b>Please transfer to below Bank Details</b><br/>
Bank Name : <b>HDFC Bank Ltd</b><br/>
HDFC Bank Current a/c No : <b>50200018112854</b><br/>
Beneficiary Name : <b>FINGERTIPPLUS TECHNOLOGIES PVT LTD</b><br/>
Bank IFSC Code : <b>HDFC0001208</b><br/>
Bank Address : 70/2, Millers Boulevard, Millers Road, Bangalore-560052<br/>
Branch and Branch Code : Millers Road Branch and 1208<br/>
Bank State / Province : Karnataka, India</p>"""


class AccountMove(models.Model):
    _inherit = 'account.move'

    narration = fields.Html(
        string="Terms and Conditions",
        compute='_compute_narration',
        store=True, readonly=True, precompute=True)

    total_hours = fields.Float(
        string="Total Hours",
        compute="_compute_total_hours",
        store=True
    )

    cgst_amount = fields.Monetary(
        string="CGST Amount",
        compute="_compute_gst_amounts",
        store=True
    )

    sgst_amount = fields.Monetary(
        string="SGST Amount",
        compute="_compute_gst_amounts",
        store=True
    )

    amount_in_words = fields.Char(
        string="Amount in Words",
        compute="_compute_amount_in_words"
    )

    @api.depends('company_id')
    def _compute_narration(self):
        for move in self:
            move.narration = DEFAULT_BANK_NOTE

    @api.depends('invoice_line_ids.hours')
    def _compute_total_hours(self):
        for move in self:
            move.total_hours = sum(move.invoice_line_ids.mapped('hours'))

    @api.depends('amount_untaxed', 'amount_tax')
    def _compute_gst_amounts(self):
        for move in self:
            # Assuming CGST + SGST split equally
            gst = move.amount_tax / 2
            move.cgst_amount = gst
            move.sgst_amount = gst

    
    @api.depends('amount_total', 'currency_id')
    def _compute_amount_in_words(self):
        for move in self:
            if move.currency_id:
                move.amount_in_words = (
                    move.currency_id.amount_to_text(move.amount_total)
                    + " Only"
                )
            else:
                move.amount_in_words = ""
