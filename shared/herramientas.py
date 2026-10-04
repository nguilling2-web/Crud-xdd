import re



VERDE = "\033[92m"
ROJO = "\033[91m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
RESET = "\033[0m"


def imprimir_titulo(texto):
    print(f"\n{AZUL}{'=' * 50}")
    print(f"{texto.center(50)}")
    print(f"{'=' * 50}{RESET}\n")


def imprimir_exito(mensaje):
    print(f"{VERDE}✓ {mensaje}{RESET}")


def imprimir_error(mensaje):
    print(f"{ROJO}✗ {mensaje}{RESET}")


def imprimir_info(mensaje):
    print(f"{AMARILLO}→ {mensaje}{RESET}")



def confirmar(mensaje):
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()

    return respuesta == "s"



def es_email_valido(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(patron, email) is not None