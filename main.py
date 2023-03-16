from fastapi import FastAPI, Body

#crear aplicación
app = FastAPI()
#modificar documentación creada con Swagger :port/docs
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, 
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
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
def create_movie(id : int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float  = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies

@app.put('/movies/{id}', tags=['movies'])
def modify_movie(id : int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float  = Body(), category: str = Body()):
    for movie in movies:
        if movie['id'] == id:
            movies['id'] = id
            movies['title'] = title
            movies['overview'] = overview
            movies['year'] = year
            movies['rating'] = rating
            movies['category'] = category
    return movies

@app.delete('/movies/{id}',tags=['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies