from abc import ABC,abstractmethod





class BaseController(ABC):



    @abstractmethod
    async def process(self):
        pass

    @abstractmethod
    async def validate(self):
        pass



