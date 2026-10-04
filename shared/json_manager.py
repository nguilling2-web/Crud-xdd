import json
import os


class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        self.ruta = ruta

        carpeta = os.path.dirname(ruta)

        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)


    def leer(self):
        # Si todavía no existe el archivo, devuelve una lista vacía
        if not os.path.exists(self.ruta):
            return []

        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            return datos if isinstance(datos, list) else []

        except (json.JSONDecodeError, OSError):
            return []


    def guardar(self, datos):
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            return True

        except (TypeError, OSError):
            return False