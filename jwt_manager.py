from jwt import encode, decode

def create_token(data: dict):
    #Crear token a partir de data, key es una llave creada
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    #Validar token, se decodifica el token con la llave creada y se obtienen los datos asociados
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data