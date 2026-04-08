# Exercise

# Write some python classes for the books example.

# Write a Book class with a title and author. Include a method has_author()

# Write a BookShelf class with a list of books. Include a generator method unique_authors()

from typing import Optional, Union

class Book:

    def __init__(self, title: str, published_year: Union[str, int], author: Optional[str] = None):
        self.title = title
        self.published_year = published_year
        self.author = author

    def details(self) -> str:
        print(f'The book {self.title} is written by {self.author}, published in the year {self.published_year}')
    
# b1 = Book('Atomic Habits', 'James')
b1 = Book('Atomic Habits', '2025')
# b1.details()
