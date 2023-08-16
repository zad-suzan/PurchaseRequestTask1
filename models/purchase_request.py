# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Purchase Request"

    name = fields.Char(string='Request Name', required=True,
                            states={'approved': [('readonly', True)],
                                    'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    req_by = fields.Many2one("res.users", string="Requested by", required=True, default=lambda self: self.env.user.id,
                            states={'approved': [('readonly', True)],
                                    'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    StartDate = fields.Date(string="Start Date", default=date.today(),
                            states={'approved': [('readonly', True)],
                                    'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    EndDate = fields.Date(string="End Date",
                            states={'approved': [('readonly', True)],
                                    'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    RejectionReason = fields.Text(string="Rejection Reason", readonly=True)
    orderlines = fields.One2many('purchase.request.line', 'pur_req_id',string='Order Lines',
                            states={'approved': [('readonly', True)],
                                    'reject': [('readonly', True)], 'cancel': [('readonly', True)]})
    TotalPrice = fields.Float(string="Total Price", compute='_compute_total_price', readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                               ('to_be_approved', 'To Be Approved'),
                               ('approved', 'Approved'),
                               ('reject', 'Rejected'),
                               ('cancel', 'Cancel')],
                              default="draft", string="Status")

    @api.depends('orderlines')
    def _compute_total_price(self):
        for rec in self:
            sum = 0
            for order in rec.orderlines:
                sum += order.Total
            rec.TotalPrice=sum

    def submit_for_approval(self):
        self.state= "to_be_approved"

    def action_to_cancel(self):
        self.state= "cancel"

    def approve(self):
        # On click approve button, change the state and send an email to purchase_manager group
        self.state= "approved"
        purchase_managers = self.env.ref('Purchase.group_purchase_manager').users
        recipients = purchase_managers.mapped('partner_id.email')
        subject = f"Purchase Request ({self.name}) has been approved"
        body = f"Dear Purchase Manager,\n\nThe purchase request ({self.name}) has been approved.\n\nBest regards and have a great day."
        self.env['mail.mail'].create({
            'subject': subject,
            'body_html': body,
            'email_to': ','.join(recipients)
        })

    def reject(self):
        self.state= "reject"

    def reset_to_draft(self):
        self.state= "draft"
