import sys, os


def resource_path(relative_path):
    """Obtiene la ruta del recurso, compatible con PyInstaller"""
    try:
        # Cuando el ejecutable está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Cuando se ejecuta en modo desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
