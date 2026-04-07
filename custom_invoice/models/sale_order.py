from odoo import models, fields, api
from datetime import datetime

DEFAULT_BANK_NOTE = """<p><b>Please transfer to below Bank Details</b><br/>
Bank Name : <b>HDFC Bank Ltd</b><br/>
HDFC Bank Current a/c No : <b>50200018112854</b><br/>
Beneficiary Name : <b>FINGERTIPPLUS TECHNOLOGIES PVT LTD</b><br/>
Bank IFSC Code : <b>HDFC0001208</b><br/>
Bank Address : 70/2, Millers Boulevard, Millers Road, Bangalore-560052<br/>
Branch and Branch Code : Millers Road Branch and 1208<br/>
Bank State / Province : Karnataka, India</p>"""


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    note = fields.Html(
        string="Terms and conditions",
        compute='_compute_note',
        store=True, readonly=True, precompute=True)

    @api.depends('partner_id')
    def _compute_note(self):
        for order in self:
            order.note = DEFAULT_BANK_NOTE

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                now = datetime.now()

                year = now.year % 100
                next_year = (now.year + 1) % 100

                prefix = f"FTPPL/PI/{year:02d}-{next_year:02d}/"

                seq = self.env['ir.sequence'].next_by_code('sale.order') or '001'

                vals['name'] = prefix + seq

        return super().create(vals_list)
