from abc import ABC, abstractmethod


class BaseProcess(ABC):
    @abstractmethod
    def validate_data(self):
        pass

    @abstractmethod
    def process_data(self):
        pass

    def execute(self):
        pass
