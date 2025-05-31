from task4 import BankAccount

def test_2():

    acc = BankAccount("Charlie", 100)
    # acc.deposit("fifty") # CustomTypeError: Deposit amount must be a number
    acc.deposit(-10)

def test_3():
    acc1 = BankAccount("Dana", 40)
    acc2 = BankAccount("Eli", 40)
    # AssertionError: Cannot transfer more than available balance
    acc1.transfer_to(acc2, 100) 
    # CustomTypeError: Target must be a BankAccount instance
    acc1.transfer_to("not-an-account", 10)


# test_3()

# class Dog:
#     dogs_created = 0

#     @classmethod
#     def create_dog(cls):
#         cls.dogs_created += 1
#         return cls()

class Dog:
    dogs_created = 0

    # @classmethod
    def create_dog(self):
        self.dogs_created += 1
        
    @classmethod
    def create_dog(cls):
        cls.dogs_created += 1
        # return cls()
    
# dog1 = Dog()
# dog1.create_dog()
# dog1.create_dog()
# dog1.create_dog()
# print(dog1.dogs_created)
# Dog.create_dog()
# print(Dog.dogs_created)
# a = set()
# a.add(1)
# print(a)
# a.clear()
# a.add(2)
# # a.remove(1)
# print(a)
# print(f"Deposit balance update failed: expected {a}, "
#     f"got {a} (previous balance: {a}, deposit amount: {a})")

print(-(-10//5))