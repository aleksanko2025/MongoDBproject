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
        ruta_id = input("RutaID (ej: RT-006): ").strip().upper()
        nombre = input("Nombre de la ruta: ")
        descripcion = input("Descripción: ")

        #Ruta activa o no
        activo = False
        estado = input("¿Está activa? (s/n): ").strip().lower()
        if estado == "s":
            activo = True
        else:
            activo = False

        duracion = int(input("Duración en horas: "))

        # Insertamos fecha
        fechas = []
        print("Introduce fechas disponibles (formato AAAA-MM-DD). Escribe 'fin' para terminar.")
        bandera1 = False
        while bandera1 != True:
            fecha = input("> Fecha: ")
            if fecha.lower() == "fin":
                bandera1 = True
            fechas.append(fecha)

        # Precio
        print("Introduce los precios:")
        adulto = float(input("Precio adulto: "))
        niño = float(input("Precio niño: "))
        moneda = input("Moneda (ej: USD): ").upper()
        precio = {"adulto": adulto, "niño": niño, "moneda": moneda}

        # Incluye
        incluye = []
        print("¿Qué incluye la ruta? Escribe 'fin' para terminar.")
        bandera2 = False
        while bandera2 != True:
            item = input("> Incluye: ")
            if item.lower() == "fin":
                bandera2 = True
            incluye.append(item)

        # Idiomas disponibles
        idiomas = []
        print("Introduce idiomas disponibles. Escribe 'fin' para terminar.")
        bandera3 = False
        while bandera3 != True:
            idioma = input("> Idioma: ")
            if idioma.lower() == "fin":
                bandera3 = True
            idiomas.append(idioma)

        # Valoraciones
        valoraciones = []
        print("Introduce una o más valoraciones. Escribe 'fin' como usuario para terminar.")

        while True:
            usuario = input("Usuario: ")
            if usuario.lower() == "fin":
                break  # Sale del bucle porque poniendo bandera se siguen ejecutando el resto de inputs
            
            comentario = input("Comentario: ")
            puntuacion = float(input("Puntuación (0-5): "))
            fecha_val = input("Fecha (AAAA-MM-DD): ")

            valoraciones.append({
                "usuario": usuario,
                "comentario": comentario,
                "puntuacion": puntuacion,
                "fecha": fecha_val
            })

        # Accesibilidad
        print("¿Accesibilidad?")
        silla = False
        silla_sino = input("¿Silla de ruedas (s/n)? ").strip().lower()
        if silla_sino == "s":
            activo = True
        else:
            activo = False
        señas = False
        señas_sino = input("¿Traducción en lengua de señas (s/n)? ").strip().lower() 
        if señas_sino == "s":
            activo = True
        else:
            activo = False
        baños = False
        baños_sino = input("¿Baños adaptados (s/n)? ").strip().lower() 
        if baños_sino == "s":
            activo = True
        else:
            activo = False
        accesibilidad = {
            "sillaDeRuedas": silla,
            "traduccionEnLenguaDeSeñas": señas,
            "bañosAdaptados": baños
        }

        # Insertando
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
        print("\n Documento insertado con éxito.")

    except Exception as e:
        print(" Error al insertar la ruta:", e)


def mostrar_rutas():
    try:
        consulta = coleccion.find({}, {"_id": 0, "rutaId": 1, "nombre": 1})

        print("\n--- Lista de Rutas ---")
        for doc in consulta:
            ruta_id = doc.get("rutaId", "Sin ID") #Si hace bien el get devuelve rutaId y si no lo encuentra pone Sin ID
            nombre = doc.get("nombre", "Sin nombre")
            print(f"RutaID: {ruta_id} | Nombre: {nombre}")

    except Exception as e:
        print("No se ha podido realizar la consulta:", e)



def borrar():
    id = input("Indique rutaID para actualizar su estado (ej: RT-001) --> ").strip().upper()

    try:
        eliminar = coleccion.delete_one({"rutaId": id}) #Consulta
        if eliminar:
            print(f"La ruta con ID {id}, se ha borrado con éxito.")
            
        else:
            print(f"No se encontró ninguna ruta con {id}")
    
    except Exception as e:
        print("Error al eliminar: ", e)


def actualizar():
    id = input("Indique rutaID para actualizar su estado (ej: RT-001) --> ").strip().upper()
    estado = input("Indique true/false si quiere activar o desactivar la ruta --> ")
    
    if estado not in ["true", "false"]:
        print("Entrada no válida. Debe ingresar 'true' o 'false'.")
        return

    try:
        resultado = coleccion.update_one({"rutaId": id}, {"$set": {"activo": estado}})
        
        if resultado.modified_count > 0:
            print(f"¡La ruta {id} se ha actualizado con éxito!")
        else:
            print("No se encontró la ruta o el valor ya era el mismo.")
    
    except Exception as e:
        print("Error al actualizar:", e)


def buscar_por_id():

    id = input("Indique rutaID para actualizar su estado (ej: RT-001) --> ").strip().upper()

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

def ruta_esta_activa():
    id = input("Indique rutaID para actualizar su estado (ej: RT-001) --> ").strip().upper()

    try:
        resultado = coleccion.find_one({"rutaId": id}, {"_id": 0, "rutaId": 1, "nombre": 1, "activo": 1})

        if resultado:
            if resultado.get("activo", False):
                print(f"La ruta '{resultado['nombre']}' (ID: {resultado['rutaId']}) está activa.")
            else:
                print(f"La ruta '{resultado['nombre']}' (ID: {resultado['rutaId']}) no está activa.")
        else:
            print("No se encontró ninguna ruta con ese ID.")

    except Exception as e:
        print("Error al consultar el estado de la ruta:", e)


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
        print("2. Mostrar el nombre de todas las rutas")
        print("3. Buscar ruta por ID")
        print("4. Buscar rutas por idioma disponible")
        print("5. Mostrar rutas accesibles con silla de ruedas")
        print("6. Disponibilidad de la ruta")
        print("7. Actualizar estado de una ruta (activo/inactivo)")
        print("8. Eliminar una ruta por ID")
        print("9. Salir")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            insertar_ruta()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "2":
            mostrar_rutas()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "3":
            buscar_por_id()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "4":
            idiomas_disponibles()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "5":
            rutas_accesibles_silla_ruedas()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "6":
            ruta_esta_activa()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "7":
            actualizar()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "8":
            borrar()
            input("Presiones 'Enter' para continuar.")
        elif opcion == "9":
            bandera = True
            print("Saliendo del programa...")
        else:
            print("Opción no válida. Intente de nuevo.")