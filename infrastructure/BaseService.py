from abc import ABC , abstractmethod




class BaseService(ABC):

    @abstractmethod
    async def validate (self):

        pass



    @abstractmethod
    async def process(self):
        pass

