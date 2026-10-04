


from models import CAMPOS_ESTUDIANTE

from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    obtener_promedio_estudiante,
    materias_ofertadas,
    estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):

    print(
        f"{'ID':<5}"
        f"{'NOMBRE':<25}"
        f"{'EMAIL':<30}"
        f"{'CARNET':<18}"
        f"{'PROMEDIO':<10}"
    )

    print("-" * 88)

    for estudiante in estudiantes:

        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<30}"
            f"{estudiante.carnet:<18}"
            f"{estudiante.obtener_promedio():<10}"
        )

    print("-" * 88)

    imprimir_info(
        f"Total: {len(estudiantes)} estudiante(s)"
    )


# =========================================================
# CREAR
# =========================================================

def opcion_crear():

    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    datos = {}

    # TUPLA de campos.
    for campo in CAMPOS_ESTUDIANTE:

        datos[campo] = input(
            f"{campo.capitalize()}: "
        )

    exito, mensaje = crear_estudiante(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# =========================================================
# VER TODOS
# =========================================================

def opcion_ver_todos():

    imprimir_titulo("LISTA DE ESTUDIANTES")

    estudiantes = obtener_todos()

    if not estudiantes:

        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )

    else:

        mostrar_tabla(estudiantes)

    pausa()


# =========================================================
# BUSCAR
# =========================================================

def opcion_buscar():

    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input(
        "Nombre, apellido, email o carnet: "
    )

    encontrados = buscar_estudiantes(termino)

    if not encontrados:

        imprimir_info(
            f"Ningún estudiante coincide con '{termino}'."
        )

    else:

        mostrar_tabla(encontrados)

    pausa()


# =========================================================
# VER POR ID
# =========================================================

def opcion_ver_por_id():

    imprimir_titulo("VER ESTUDIANTE POR ID")

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )

    else:

        # DICCIONARIO:
        # recorremos clave y valor.
        for clave, valor in estudiante.a_diccionario().items():

            print(
                f"  {clave.capitalize():<12}: {valor}"
            )

    pausa()


# =========================================================
# ACTUALIZAR
# =========================================================

def opcion_actualizar():

    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )

        return pausa()

    imprimir_info(
        f"Editando a {estudiante.obtener_nombre_completo()}"
    )

    print(
        "Deje en blanco el campo que no quiera cambiar.\n"
    )

    # DICCIONARIO de cambios.
    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:

        actual = getattr(estudiante, campo)

        nuevo = input(
            f"{campo.capitalize()} [{actual}]: "
        ).strip()

        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(
        id_estudiante,
        cambios
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# =========================================================
# ELIMINAR
# =========================================================

def opcion_eliminar():

    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    estudiante = obtener_por_id(id_estudiante)

    if not estudiante:

        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )

        return pausa()

    imprimir_info(
        f"Se eliminará: {estudiante}"
    )

    if confirmar("¿Confirma la eliminación?"):

        exito, mensaje = eliminar_estudiante(
            id_estudiante
        )

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    else:

        imprimir_info("Operación cancelada")

    pausa()


# =========================================================
# AGREGAR NOTA
# =========================================================

def opcion_agregar_nota():

    imprimir_titulo("AGREGAR NOTA")

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    materia = input(
        "Materia: "
    )

    nota = input(
        "Nota (0 - 20): "
    )

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# =========================================================
# VER PROMEDIO
# =========================================================

def opcion_ver_promedio():

    imprimir_titulo("VER PROMEDIO")

    try:

        id_estudiante = int(
            input("Id del estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        return pausa()

    exito, resultado = obtener_promedio_estudiante(
        id_estudiante
    )

    if not exito:

        imprimir_error(resultado)

    else:

        estudiante = obtener_por_id(id_estudiante)

        imprimir_info(
            f"Estudiante: "
            f"{estudiante.obtener_nombre_completo()}"
        )

        imprimir_exito(
            f"Promedio: {resultado}"
        )

    pausa()


# =========================================================
# MATERIAS EN COMÚN
# =========================================================

def opcion_materias_comun():

    imprimir_titulo("MATERIAS EN COMÚN")

    try:

        id_a = int(
            input("Id del primer estudiante: ")
        )

        id_b = int(
            input("Id del segundo estudiante: ")
        )

    except ValueError:

        imprimir_error(
            "Los ids deben ser números enteros"
        )

        return pausa()

    exito, resultado = estudiantes_en_comun(
        id_a,
        id_b
    )

    if not exito:

        imprimir_error(resultado)

    elif not resultado:

        imprimir_info(
            "Los estudiantes no comparten materias."
        )

    else:

        imprimir_exito(
            "Materias en común: "
            + ", ".join(sorted(resultado))
        )

    pausa()


# =========================================================
# MATERIAS OFERTADAS
# =========================================================

def opcion_materias_ofertadas():

    imprimir_titulo("MATERIAS OFERTADAS")

    materias = materias_ofertadas()

    if not materias:

        imprimir_info(
            "Todavía no existen materias registradas."
        )

    else:

        print()

        for materia in sorted(materias):

            print(f"  - {materia}")

        imprimir_info(
            f"Total: {len(materias)} materia(s)"
        )

    pausa()


# =========================================================
# SALIR
# =========================================================

def salir():

    imprimir_info("¡Hasta luego! 👋")

    return "salir"


# =========================================================
# MENÚ
# =========================================================

# DICCIONARIO:
# relaciona cada opción con una función.
OPCIONES = {

    "1": (
        "Crear estudiante",
        opcion_crear
    ),

    "2": (
        "Ver todos",
        opcion_ver_todos
    ),

    "3": (
        "Buscar estudiante",
        opcion_buscar
    ),

    "4": (
        "Ver por id",
        opcion_ver_por_id
    ),

    "5": (
        "Actualizar estudiante",
        opcion_actualizar
    ),

    "6": (
        "Eliminar estudiante",
        opcion_eliminar
    ),

    "7": (
        "Agregar nota",
        opcion_agregar_nota
    ),

    "8": (
        "Ver promedio",
        opcion_ver_promedio
    ),

    "9": (
        "Materias en común",
        opcion_materias_comun
    ),

    "10": (
        "Materias ofertadas",
        opcion_materias_ofertadas
    ),

    "0": (
        "Salir",
        salir
    ),
}


def mostrar_menu():

    imprimir_titulo(
        "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    )

    for tecla, (texto, _funcion) in OPCIONES.items():

        print(
            f"  {tecla}. {texto}"
        )

    print()


def main():

    while True:

        mostrar_menu()

        tecla = input(
            "Seleccione una opción: "
        ).strip()

        if tecla not in OPCIONES:

            imprimir_error(
                "Opción no válida"
            )

            pausa()

            continue

        _texto, funcion = OPCIONES[tecla]

        if funcion() == "salir":
            break


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nPrograma interrumpido por el usuario."
        )