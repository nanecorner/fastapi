from fastapi import FastAPI

#crear aplicación
app = FastAPI()

@app.get('/')
def message():
    return "Hello World!"