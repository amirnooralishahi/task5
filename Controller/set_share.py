from hepler.helper_parcel import get_and_check_entity
from repository.Vendor import RepositoryVendor


class setShare:


    def __init__(self,vendor_id:int,num:int):
        self.vendor_id = vendor_id
        self.num = num


    async def process(self):
        query_vendor = await get_and_check_entity(
            RepositoryVendor,
            identifier=self.vendor_id,
        )

        percent = self.num / 100
        name = {query_vendor.name}
        last_name = {query_vendor.last_name}
        if query_vendor.share != None:
            update_share = RepositoryVendor.update_by_id(self.vendor_id, {'share': query_vendor.share})
            return {'message': f'share {percent} with successfully updated for {name}{last_name} '}

        update_share = await RepositoryVendor.update_by_id(self.vendor_id, {'share': percent})
        return {'message': f'share {percent} with successfully submit for {name} {last_name} '}