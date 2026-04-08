import pickle

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"
    
person1 = Person('Alice', 39)

def pickle_object():
    with open('pickle.pkl', 'wb') as fs:
        pickle.dump(person1, fs)
    print('object pickled sucess')

# pickle_object()

def extract_object():
    with open('pickle.pkl', 'rb') as fs:
        data = pickle.load(fs)
        print(data)
    
    print('object extracted sucess')

# extract_object()

import json

data = {"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"]}

def save_json():
    with open('data.json', 'w') as fs:
        json.dump(data, fs)
    print('Data saved as JSON.')

# save_json()

def load_data():
    with open('data.json', 'r') as fs:
        data = json.load(fs)
    print(data)

# load_data()





