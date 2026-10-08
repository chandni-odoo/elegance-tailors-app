from odoo import models, api


class DepositReceipt(models.AbstractModel):
    _name = 'report.tailoring_app.report_deposit_receipt'
    _description = 'Deposit Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        if not docids:
            docids = self.env.context.get('active_ids') or []

        records = self.env['tailor.order.deposit.history'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'tailor.order.deposit.history',
            'docs': records,
        }


class TailorOrderpant(models.AbstractModel):
    _name = 'report.tailoring_app.report_pant_measurement'
    _description = 'Pant Measurement Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        if not docids:
            docids = self.env.context.get('active_ids') or []

        records = self.env['tailor.order'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'tailor.order',
            'docs': records,
        }

class TailorOrderShirt(models.AbstractModel):
    _name = 'report.tailoring_app.report_shirt_measurement'
    _description = 'Shirt Measurement Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        if not docids:
            docids = self.env.context.get('active_ids') or []

        records = self.env['tailor.order'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'tailor.order',
            'docs': records,
        }

