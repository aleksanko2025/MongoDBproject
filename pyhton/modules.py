from pymongo import MongoClient

def conectar():

    global db, documento

    try:
        client = MongoClient("mongodb://localhost:27017/") 

        db = client["turismo"] # Accede a la base de datos

        coleccion = db["rutas"] # Accede a la colección

        documento = coleccion.find_one() # Ahora puedes hacer operaciones

        print("¡Conexión establecida con éxito!")

    except Exception as e:
        
        print("No se ha podidio establecer la conexión")

def buscar_por_nombre():



