from pydantic import BaseModel, Field
import json 

class Book(BaseModel):
    title: str
    author: str
    pages: int 
    published: bool = True 

    def summarize(book) -> str:
        print(f'The book {book.title} is written by author {book.author}, which has {book.pages} pages')

input_data = {
    'title': 'Atomic habits',
    'author': 'james clear',
    'pages': 200,
    'published': True
}

book1 = Book(**input_data)
# book1.summarize()

# print(book1)
# print(book1.model_dump())
# print(book1.model_dump_json())

# 4. Write a function
# Write a function def summarize(book: Book) -> str: that returns a string summary of a book object.



# Exercises

# Movie model 

# 1. Create a Movie model

# 5. Bonus: Validation 

class Movie(BaseModel):
    title: str = Field(..., max_length=100)
    year: int
    genres: str
    duration_minutes: int
    rating: float = Field(..., ge=1.0, le=10.0)

movie_data = {
    'title': 'Dhurandhar',
    'year': 2025,
    'genres' : 'Action',
    'duration_minutes': 214,
    'rating' : 1.0
}

dhurandhar_movie = Movie(**movie_data)
print(dhurandhar_movie)

# 2. Parse from JSON 
# Write a JSON string for a Movie, load it with json.loads(), and parse it into a Pydantic model.

def parse_json(data):
    json_string = json.dumps(data.model_dump())
    json_data = json.loads(json_string)
    new_obj = Movie(**json_data)
    return new_obj

movie_obj = parse_json(dhurandhar_movie)
print(movie_obj)

# 3. Use nested models

class Director(BaseModel):
    name: str
    born: int 

class MovieNest(BaseModel):
    title: str 
    director: Director

director_movie_data = {
    'title': 'Dhurandhar',
    'director': {
        'name': 'Aditya Dhar',
        'born': 1983,
    }
}

director_movie = MovieNest(**director_movie_data)
print(director_movie)

