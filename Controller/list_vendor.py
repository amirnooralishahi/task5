from repository.Vendor import RepositoryVendor
from schema.SchemaVendor import ShowVendorSchema


class listVendor:

    def __init__(self):
        pass

    async def process(self):
        execute = await  RepositoryVendor.all()
        vendor_list = []

        for item in execute:
            show = ShowVendorSchema(
                id=item.id,
                name=item.name,
                last_name=item.last_name,
                phone=item.phone,
                balance=item.balance,

            )
            vendor_list.append(show)
        return vendor_list