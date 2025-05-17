from pymongo import MongoClient

def conectar():

    global db, coleccion

    try:
        client = MongoClient("mongodb://localhost:27017/") 

        db = client["turismo"] # Accede a la base de datos

        coleccion = db["rutas"] # Accede a la colección

        print("¡Conexión establecida con éxito!")

    except Exception as e:
        
        print("No se ha podidio establecer la conexión")


def insertar_ruta():
    try:
        ruta_id = input("RutaID (ej: RT-006): ")
        nombre = input("Nombre de la ruta: ")
        descripcion = input("Descripción: ")
        activo = input("¿Está activa? (True/False): ").strip().lower() == "true"
        duracion = int(input("Duración en horas (número): "))

        # Lista de fechas (usamos ast.literal_eval para evaluar lista como string)
        fechas = input("Fechas disponibles (ej: ['2025-06-12', '2025-06-19']): ")

        # Precio (diccionario con adulto, niño y moneda)
        precio = input("Precio (ej: {'adulto': 19, 'niño': 10, 'moneda': 'USD'}): ")

        # Incluye (lista)
        incluye = input("¿Qué incluye? (lista, ej: ['Guía', 'Bicicleta']): ")

        # Idiomas disponibles
        idiomas = input("Idiomas disponibles (ej: ['español', 'inglés']): ")

        # Valoraciones (puede ser lista con un solo dict)
        valoraciones = input("Valoraciones (ej: [{'usuario': 'juan', 'comentario': 'Muy buena', 'puntuacion': 4.5, 'fecha': '2025-04-25'}]): ")

        # Accesibilidad (diccionario)
        accesibilidad = input("Accesibilidad (ej: {'sillaDeRuedas': True, 'traduccionEnLenguaDeSeñas': True, 'bañosAdaptados': True}): ")

        nuevo_doc = {
            "rutaId": ruta_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "activo": activo,
            "duracionHoras": duracion,
            "fechaDisponible": fechas,
            "precio": precio,
            "incluye": incluye,
            "idiomasDisponibles": idiomas,
            "valoraciones": valoraciones,
            "accesibilidad": accesibilidad
        }
        
        coleccion.insert_one(nuevo_doc)
        print("Documento insertado con éxito.")
    except Exception as e:
        print("Error al insertar la ruta:", e)



def borrar():
    id = input("Indique rutaID para eliminar (ej: RT-001) --> ")

    try:
        eliminar = coleccion.delete_one({"rutaId": id}) #Consulta
        if eliminar:
            print(f"La ruta con ID {id}, se ha borrado con éxito.")
            
        else:
            print(f"No se encontró ninguna ruta con {id}")
    
    except Exception as e:
        print("Error al eliminar: ", e)


def actualizar():
    id = input("Indique rutaID para actualziar su estado (ej: RT-001) --> ")
    estado = input("Indique true/false si quire activar o desactivar la ruta --> ")

    try:
        actualizar = coleccion.update_one({"rutaId": {id}}, {"$set": {"activo": estado}})
        if actualizar:
            print(f"¡La ruta {id} se ha actualizado con éxito!")
        else:
            print("No se encontró ruta con ese ID o el tipo de estado indicado no existe")
    
    except Exception as e:
        print("Error al actualziar: ", e)

def buscar_por_id():

    id = input("Indique rutaID para buscar (ej: RT-001) --> ")

    try:
        resultado = coleccion.find_one({"rutaId": id}) #Consulta
        if resultado:
            print("\n")
            for clave, valor in resultado.items():
                print(f"{clave}: {valor}")
        else:
            print(f"No se encontró ninguna ruta con {id}")
    
    except Exception as e:
        print("Error al relaizar la búsqueda: ", e)

def idiomas_disponibles():
    idioma = input("Indique el idioma que busca para una ruta --> ").strip()

    try:
        cursor = coleccion.find(
            {"idiomasDisponibles": idioma},
            {"_id": 0, "nombre": 1, "idiomasDisponibles": 1}
        )

        resultados = list(cursor)  #Convertimos cursor en lista

        if resultados:
            for doc in resultados:
                print("\nRuta encontrada:")
                for k, v in doc.items():
                    print(f"{k}: {v}")
        else:
            print("Idioma no disponible en ninguna ruta.")

    except Exception as e:
        print("Error al hacer la búsqueda:", e)

def rutas_accesibles_silla_ruedas():
    try:
        resultados = coleccion.find(
            {"accesibilidad.sillaDeRuedas": True},
            {"_id": 0, "nombre": 1, "accesibilidad": 1}
        )

        resultados = list(resultados)

        if resultados:
            print("\nRutas accesibles con silla de ruedas:")
            for doc in resultados:
                print(f"\nNombre: {doc.get('nombre')}")
                print("Accesibilidad:")
                for clave, valor in doc.get("accesibilidad", {}).items():
                    print(f"  {clave}: {valor}")
        else:
            print("No hay rutas con acceso para silla de ruedas.")

    except Exception as e:
        print("Error al buscar rutas accesibles:", e)

def menu():

    bandera = False

    while bandera != True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Insertar nueva ruta")
        print("2. Buscar ruta por ID")
        print("3. Buscar rutas por idioma disponible")
        print("4. Mostrar rutas accesibles con silla de ruedas")
        print("5. Actualizar estado de una ruta (activo/inactivo)")
        print("6. Eliminar una ruta por ID")
        print("7. Salir")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            insertar_ruta()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "2":
            buscar_por_id()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "3":
            idiomas_disponibles()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "4":
            rutas_accesibles_silla_ruedas()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "5":
            actualizar()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "6":
            borrar()
        elif opcion == "7":
            bandera = True
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")