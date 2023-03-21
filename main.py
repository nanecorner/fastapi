from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, Field
from typing  import Optional


#crear aplicación
app = FastAPI()
#modificar documentación creada con Swagger :port/docs
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
#Para acceder a sistema de documentación /docs

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(minlength=1)
    overview: str
    year: int = Field(le=2022)
    rating: float = Field(ge=0, le=10)
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción",
                "year": 0,
                "rating": 0.0,
                "category": "sin categoría" 
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 9.4,
        'category': 'Acción'    
    }, 
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi 2, seres que ...",
        'year': 2022,
        'rating': 8.9,
        'category': 'Acción'    
    } 
]

#decorador get, ruta y etiqueta en documentación
@app.get('/', tags=['home'])
def message():
    return "Hello World!"

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}',tags=['movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id']==id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    for movie in movies:
        if movie['category'] == category:
            return movie
    return []

@app.post('/movies', tags = ['movies'])
# Datos con Body 
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

# Agregar un modelo
@app.put('/movies/{id}', tags=['movies'])
def modify_movie(id : int, movie: Movie):
    for movie in movies:
        if movie['id'] == id:
            movies['id'] = id
            movies['title'] = movie.title
            movies['overview'] = movie.overview
            movies['year'] = movie.year
            movies['rating'] = movie.rating
            movies['category'] = movie.category
    return movies

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies