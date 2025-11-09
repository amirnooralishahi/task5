from abc import ABC , abstractmethod




class BaseService(ABC):

    @abstractmethod
    async def validate (self):
        pass


    @abstractmethod
    def response(self):
        pass


    @abstractmethod
    async def fetch_data (self):
        pass

    @abstractmethod
    async def process(self):
        pass

