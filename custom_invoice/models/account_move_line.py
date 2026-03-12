from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    hours = fields.Float(string="Hours")
    sac_code = fields.Char(string="SAC Code")
