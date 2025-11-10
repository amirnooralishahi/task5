from service.cancel_invoice_service import CancelInvoiceService


class cancelInvoice:

    def __init__(self, name, last_name, invoice):
        self.name = name
        self.last_name = last_name
        self.invoice_id = invoice

    async def process(self):
        service = CancelInvoiceService(self.name, self.last_name, self.invoice_id)
        return await service.response()
