from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# El proyecto de estudiantes usa su propio archivo JSON.
gestor = GestorJSON("data/estudiantes.json")


# TUPLAS:
# Son datos fijos que no necesitamos modificar.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")

CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# =========================================================
# AYUDAS INTERNAS
# =========================================================

def emails_registrados(excepto_id=None):
    """
    SET de emails registrados.
    Permite detectar rápidamente si un email está repetido.
    """
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def carnets_registrados(excepto_id=None):
    """
    SET de carnets registrados.
    Un carnet no puede pertenecer a dos estudiantes.
    """
    return {
        registro["carnet"].upper()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    """
    LISTA de ids para determinar cuál será
    el siguiente identificador.
    """
    ids = [registro["id"] for registro in gestor.leer()]

    return max(ids) + 1 if ids else 1


# =========================================================
# C · CREATE
# =========================================================

def crear_estudiante(datos):
    """
    Recibe un DICCIONARIO con los datos del estudiante.
    Devuelve una TUPLA:
    (True/False, mensaje)
    """

    try:

        # DICCIONARIO:
        # normalizamos todos los campos recibidos.
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_ESTUDIANTE
        }

        # Verificar campos obligatorios.
        faltantes = [
            campo
            for campo in CAMPOS_OBLIGATORIOS
            if not valores[campo]
        ]

        if faltantes:
            return (
                False,
                f"Faltan campos obligatorios: {', '.join(faltantes)}"
            )

        # Validar email.
        if not es_email_valido(valores["email"]):
            return (
                False,
                f"El email '{valores['email']}' no tiene un formato válido"
            )

        # SET para comprobar email duplicado.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        # SET para comprobar carnet duplicado.
        if valores["carnet"].upper() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # Creamos el objeto del Modelo.
        estudiante = Estudiante(
            siguiente_id(),
            **valores
        )

        # LISTA de registros.
        registros = gestor.leer()

        registros.append(
            estudiante.a_diccionario()
        )

        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return (
            True,
            f"Estudiante {estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# =========================================================
# R · READ
# =========================================================

def obtener_todos():
    """
    Devuelve una LISTA de objetos Estudiante.
    """

    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_estudiante):
    """
    Busca un estudiante por id.
    """

    for estudiante in obtener_todos():

        if estudiante.id == id_estudiante:
            return estudiante

    return None


# =========================================================
# S · SEARCH
# =========================================================

def buscar_estudiantes(termino):
    """
    Realiza una búsqueda lineal utilizando
    la TUPLA CAMPOS_BUSCABLES.
    """

    termino = termino.strip().lower()

    if not termino:
        return []

    encontrados = []

    for registro in gestor.leer():

        for campo in CAMPOS_BUSCABLES:

            if termino in str(
                registro.get(campo, "")
            ).lower():

                encontrados.append(
                    Estudiante.desde_diccionario(registro)
                )

                break

    return encontrados


# =========================================================
# U · UPDATE
# =========================================================

def actualizar_estudiante(id_estudiante, cambios):
    """
    Actualiza los datos de un estudiante.
    """

    try:

        # SET:
        # diferencia de conjuntos para detectar campos inválidos.
        desconocidos = (
            set(cambios) - set(CAMPOS_ESTUDIANTE)
        )

        if desconocidos:
            return (
                False,
                f"Campos no válidos: "
                f"{', '.join(sorted(desconocidos))}"
            )

        if not cambios:
            return False, "No se indicó ningún cambio"

        # Limpiamos espacios.
        cambios = {
            campo: str(valor).strip()
            for campo, valor in cambios.items()
        }

        # No permitimos dejar campos obligatorios vacíos.
        for campo in CAMPOS_OBLIGATORIOS:

            if campo in cambios and not cambios[campo]:
                return False, f"El campo {campo} no puede estar vacío"

        # Validación de email.
        if "email" in cambios:

            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

            if (
                cambios["email"].lower()
                in emails_registrados(excepto_id=id_estudiante)
            ):
                return False, "Ese email ya lo usa otro estudiante"

        # Validación de carnet.
        if "carnet" in cambios:

            if (
                cambios["carnet"].upper()
                in carnets_registrados(excepto_id=id_estudiante)
            ):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()

        posicion = None

        for indice, registro in enumerate(registros):

            if registro["id"] == id_estudiante:
                posicion = indice
                break

        # Validación de ID inexistente.
        if posicion is None:
            return (
                False,
                f"No existe un estudiante con id {id_estudiante}"
            )

        registros[posicion].update(cambios)

        if not gestor.guardar(registros):
            return False, "No se pudo guardar el archivo"

        return (
            True,
            f"Estudiante {id_estudiante} actualizado "
            f"({len(cambios)} campo/s)"
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# =========================================================
# D · DELETE
# =========================================================

def eliminar_estudiante(id_estudiante):

    registros = gestor.leer()

    # LISTA nueva sin el estudiante eliminado.
    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    if len(quedan) == len(registros):
        return (
            False,
            f"No existe un estudiante con id {id_estudiante}"
        )

    if not gestor.guardar(quedan):
        return False, "No se pudo guardar el archivo"

    return True, f"Estudiante {id_estudiante} eliminado"


# =========================================================
# AGREGAR NOTA
# =========================================================

def agregar_nota(id_estudiante, materia, nota):

    estudiante = obtener_por_id(id_estudiante)

    # Validación de ID inexistente.
    if estudiante is None:
        return (
            False,
            f"No existe un estudiante con id {id_estudiante}"
        )

    materia = str(materia).strip()

    if not materia:
        return False, "La materia no puede estar vacía"

    # Validamos que realmente sea un número.
    try:
        nota = float(nota)

    except (ValueError, TypeError):
        return False, "La nota debe ser un número"

    # Validación solicitada: 0 - 20.
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"

    # El Modelo se encarga de:
    # 1. inscribir la materia en el SET
    # 2. agregar la nota a la LISTA correspondiente.
    estudiante.agregar_nota(materia, nota)

    registros = gestor.leer()

    for indice, registro in enumerate(registros):

        if registro["id"] == id_estudiante:

            registros[indice] = estudiante.a_diccionario()
            break

    if not gestor.guardar(registros):
        return False, "No se pudo guardar la nota"

    return (
        True,
        f"Nota {nota} agregada en {materia}"
    )


# =========================================================
# VER PROMEDIO
# =========================================================

def obtener_promedio_estudiante(id_estudiante):

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        return (
            False,
            f"No existe un estudiante con id {id_estudiante}"
        )

    promedio = estudiante.obtener_promedio()

    return True, promedio


# =========================================================
# MATERIAS OFERTADAS
# =========================================================

def materias_ofertadas():
    """
    SET con todas las materias encontradas
    entre todos los estudiantes.

    Al ser un conjunto, ninguna materia se repite.
    """

    materias = set()

    for estudiante in obtener_todos():

        # Unión de conjuntos.
        materias.update(estudiante.materias)

    return materias


# =========================================================
# MATERIAS EN COMÚN
# =========================================================

def estudiantes_en_comun(id_a, id_b):
    """
    Devuelve la intersección de materias
    entre dos estudiantes.
    """

    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    # Validamos ambos ids.
    if estudiante_a is None:
        return (
            False,
            f"No existe un estudiante con id {id_a}"
        )

    if estudiante_b is None:
        return (
            False,
            f"No existe un estudiante con id {id_b}"
        )

    # SET & SET = intersección.
    materias_comunes = (
        estudiante_a.materias
        & estudiante_b.materias
    )

    return True, materias_comunes