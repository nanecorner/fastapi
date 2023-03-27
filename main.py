from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing  import Optional, List
import jwt_manager
from fastapi.security import HTTPBearer

#crear aplicación
app = FastAPI()
#modificar documentación creada con Swagger :port/docs
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
#Para acceder a sistema de documentación /docs

#Validación de credenciales
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = jwt_manager.validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales inválidas")

#clase de usuario
class User(BaseModel):
    email: str
    password: str

#clase de película
class Movie(BaseModel):
    #Opcionales y constraints
    id: Optional[int] = None
    title: str = Field(minlength=1)
    overview: str
    year: int = Field(le=2022)
    rating: float = Field(ge=0, le=10)
    category: str

    #"default"
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

#ruta de login
@app.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        #se crea el token
        token: str = jwt_manager.create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=404, content={"message":"Datos incorrectos"})

#ruta películas, se verifica el token
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#ruta película por id
@app.get('/movies/{id}',tags=['movies'], response_model=Movie, status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1)) -> Movie:
    for movie in movies:
        if movie['id']==id:
            return JSONResponse(status_code=200, content=movie)
    return JSONResponse(status_code=404, content=[])

#ruta películas por categoría
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str = Query(min_length=5)) -> List[Movie]:
    movie = [movie for movie in movies if movie['category']==category]
    if movie:
        return JSONResponse(status_code=200, content=movie)
    else:
        return JSONResponse(status_code=404, content=[])

#ruta para agregar películas
@app.post('/movies', tags = ['movies'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
# Datos con Body --> def create_movie(id:int=Body())
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"Se ha registrado la película"})

#ruta para modificar película, agregar un modelo
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def modify_movie(id : int, movie: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies['id'] = id
            movies['title'] = movie.title
            movies['overview'] = movie.overview
            movies['year'] = movie.year
            movies['rating'] = movie.rating
            movies['category'] = movie.category
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la película"})

#ruta para eliminar película
@app.delete('/movies/{id}',tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return JSONResponse(status_code=200, content={"message":"Se ha eliminado la película"})