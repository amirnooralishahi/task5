from infrastructure.BaseService import BaseService



class addProductService(BaseService):


    def get_data(self,name,last_name,data):
        self.name=name
        self.last_name=last_name
        self.data=data


    def validate(self):
        pass

    def process(self):
        pass

    def Response_to_controller(self):
        pass