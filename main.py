from fastapi import FastAPI

app = FastAPI()


#endpoint
@app.get("/")
def inicio():
    return ("mensaje: "Hola, estoy aprendiendo FastAPI"")