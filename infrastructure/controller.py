from abc import ABC,abstractmethod





class BaseController(ABC):


    async def process_request(self, service_class, *args, **kwargs):
        service = service_class(*args, **kwargs)
        return await service.process()
    @abstractmethod
    async def process(self):
        pass





