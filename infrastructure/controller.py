from abc import ABC,abstractmethod





class BaseController(ABC):



    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def validate(self):
        pass
    @abstractmethod
    def Response(self):
        pass


