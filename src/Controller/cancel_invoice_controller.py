from InputResponseSchema.cancel_invoice_schema import InputCancelInvoice
from service.cancel_invoice_service import CancelInvoiceService
from infrastructure.controller import BaseController


class cancelInvoice(BaseController):

    def __init__(self, name: InputCancelInvoice, last_name: InputCancelInvoice, invoice: InputCancelInvoice):
        self.name = name
        self.last_name = last_name
        self.invoice_id = invoice

    async def process(self):
        service = CancelInvoiceService(self.name, self.last_name, self.invoice_id)
        return await service.response()
