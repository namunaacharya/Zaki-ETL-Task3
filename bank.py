from abc import abstractmethod, ABC
from datetime import datetime
import json

class Bank(ABC):
    bank_name = 'Nabil Bank'

    def __init__(self, name, address, status = 'Active'):
        self.id = id(self)
        self.name = name
        self.address = address
        self.balance = 0
        self.__pin = 1234
        self.status = status
        
    @abstractmethod
    def deposit(self):
        pass

    @abstractmethod
    def withdrawal(self):
        pass

    @abstractmethod
    def transaction(self):
        pass

    def check_datatype(data_type):
        def validate(func):
            def wrapper(*args):
                if not isinstance(args[1],data_type):
                    print(f"Invalid datatype. Datatype should be {data_type}")
                    return False
                return func(*args)
            return wrapper
        return validate

    def validate_balance(func):
        def wrapper(self, amount, *args):
            if self.balance < amount:
                print("Sorry, this transaction cannot be held.")
                print(f"Insufficient balance : Rs.{self.balance}.")
                return False
            return func(self,amount, *args)
        return wrapper
    

class Customer(Bank):
    def __init__(self, name, address, status='Active'):
        super().__init__(name, address, status)

    @Bank.check_datatype(int)
    def deposit(self,amount):
        if amount < 0:
            print("Amount can't be negative.")
            return False     
        print(f"Dear {self.name}, Rs.{amount} has been deposited on your account. {Bank.bank_name} ")
        self.balance += amount
        print(f"Total Balance : Rs.{self.balance}")

    @Bank.check_datatype(int)
    @Bank.validate_balance
    def withdrawal(self,amount):
        print(f"Dear {self.name}, Rs.{amount} has been withdrawn from your account. {Bank.bank_name} ")
        self.balance -= amount
        print(f"Total Balance : Rs.{self.balance}")

    @Bank.check_datatype(int)
    @Bank.validate_balance
    def transaction(self,amount,receiver_name):  
        print(f"Dear {self.name}, Rs.{amount} has been transfered to {receiver_name}'s account. {Bank.bank_name} ")
        self.balance -= amount
        receiver.balance += amount
        print(f"Your balance : {customer.balance}")
        print(f"{receiver.name}'s balance : {receiver.balance}")

    @property
    def get_pin(self):
        return(self.__pin)
    
    @get_pin.setter
    def change_pin(self,new_pin):
        self.__pin = new_pin
        print(f"Your pin is updated.")


class Staff(Bank):
    def __init__(self, name, address, department, status='Active'):
        super().__init__(name, address, status)
        self.department = department
        self.break_time = ('13:00','14:00')
        
    @Bank.check_datatype(int)
    def deposit(self,amount):
        if amount < 0:
            print("Amount can't be negative.")
            return False     
        print(f"Dear {self.name}, Rs.{amount} has been deposited on your account. {Bank.bank_name} ")
        self.balance += amount
        print(f"Total Balance : Rs.{self.balance}")

    @Bank.check_datatype(int)
    @Bank.validate_balance
    def withdrawal(self,amount):
        print(f"Dear {self.name}, Rs.{amount} has been withdrawn from your account. {Bank.bank_name} ")
        self.balance -= amount
        print(f"Total Balance : Rs.{self.balance}")

    @Bank.check_datatype(int)
    @Bank.validate_balance
    def transaction(self,amount,receiver):  
        print(f"Dear {self.name}, Rs.{amount} has been transferred to {self.receiver}'s account. {Bank.bank_name} ")
        self.balance -= amount
        receiver.balance += amount

    @property
    def change_pin(self):
        return(self.__pin)
    
    @change_pin.setter
    def change_pin(self,new_pin):
        self.__pin = new_pin
        print(f"Your pin is updated.")

    def check_break(self,time):
        try:
            time = datetime.strptime(time, "%H:%M").time()
            break_start = datetime.strptime(self.break_time[0], "%H:%M").time()
            break_end = datetime.strptime(self.break_time[1], "%H:%M").time()
            if break_start <= time <= break_end:
                print(f"{self.name} is currently on break.")
            else:
                print(f"{self.name} is currently available.")
        except ValueError:
            print("Invalid time format. Use HH:MM.")


receiver = Customer('Prabina','Ktm')
customer = Customer('Namuna','Butwal')
staff = Staff('Yami','Kalanki','Cash')

customer.change_pin = 2345
customer.deposit(1000)
customer.transaction(200,receiver.name)

staff.withdrawal(200)
staff.check_break('13:40')
staff.check_break('40:13')

data = {}
data[customer.id] = {'name':customer.name, 'address':customer.address, 'status' : customer.status}
with open('customer_entry.json','w') as f:
    json.dump(data, f, indent=4)

data = {}
data[staff.id] = {'name':staff.name, 'address':staff.address, 'status' : staff.status}
with open('staff_entry.json','w') as f:
    json.dump(data, f, indent=4)







