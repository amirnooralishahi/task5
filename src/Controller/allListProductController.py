from src.repository.Vendor import RepositoryVendor
from src.repository.product import RepositoryProduct

class AllListProductController:



    def __init__(self):
        pass

    @classmethod
    async def process(cls):
        all_list = await RepositoryProduct.all()
        print(all_list)
        vendor_id = [value.vendor_id for value in all_list]
        name_product = [value.name for value in all_list]
        price = [value.price for value in all_list]
        get_vendor = await RepositoryVendor.find_by_many_id(vendor_id)
        vendor = {
            value.id: {'name': value.name, 'last_name': value.last_name}
            for value in get_vendor
        }
        listProduct = []
        for i in range(len(vendor_id)):
            for key, value in vendor.items():
                if vendor_id[i] == key:
                    show = {i: {
                        'nameVendor': value['name'],
                        'lastNameVendor': value['last_name'],
                        'nameProduct': name_product[i],
                        'price': price[i],
                    }}
                    listProduct.append(show)
        print(listProduct)
        return listProduct
