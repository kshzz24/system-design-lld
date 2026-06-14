from dataclasses import dataclass

@dataclass
class Movie:
    movie_name:str
    movie_id:str
    director:str
    duration:int