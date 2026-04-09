# Decorator function 

class Employee:
    raise_amount = 500

    def __init__(self, name, salary):
        self.name = name 
        self.salary = salary 
    
    @classmethod
    def change_raise(cls, new_value):
        cls.raise_amount = int(new_value)

    @staticmethod
    def add(a, b):
        return a + b
    
emp1 = Employee('raj', 12000)

print('=' * 50)
print('Before change raise fn', Employee.raise_amount)

Employee.change_raise('2000')

print('After change raise fn', Employee.raise_amount)

print('Static method in use: ', Employee.add(5,2))

print('=' * 50)

# Custom decorators

def decorator_fn(fn):
    def mfx(*args, **kwargs):
        print('Start of the fn')
        fn(*args, **kwargs)
        print('End of the fn')

    return mfx

@decorator_fn
def greet():
    print('Hello World, how are you? ')

greet()

