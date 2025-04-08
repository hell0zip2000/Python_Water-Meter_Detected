from DAO.CustomerDAO import CustomerDAO

class CustomerBUS:
    def __init__(self):
        self.customerDAO = CustomerDAO()
    
    def getAllCustomers(self):
        return self.customerDAO.getAllCustomers()
    
    def searchCustomer(self, keyword, search_type):
        return self.customerDAO.searchCustomer(keyword, search_type)