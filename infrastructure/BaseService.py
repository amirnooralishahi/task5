from abc import ABC , abstractmethod




class BaseService(ABC):

    @abstractmethod
    def validate (self):

        pass

    @abstractmethod

    def get_data(self):
        pass

    @abstractmethod
    def process(self):
        pass
    @abstractmethod
    def Response_to_controller(self):
        pass
