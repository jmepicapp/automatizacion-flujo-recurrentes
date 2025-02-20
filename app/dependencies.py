"""
app/dependencies.py
Contiene la lógica de validación de dependencias entre pasos.
En este ejemplo, se deja minimalista; podrías ampliar para
manejar estados en la BD, etc.
"""


def pasos_listos_para_ejecutar(pasos, estados):
    """
    Dado un listado de pasos y sus dependencias,
    y un diccionario con los estados (pendiente, en_progreso, completado) de cada paso,
    determina cuáles pasos pueden ejecutarse ahora.
    """
    listos = []
    for paso in pasos:
        nombre = paso["nombre"]
        if estados.get(nombre) == "pendiente":
            # Checar dependencias
            deps = paso.get("dependencias", [])
            if all(estados.get(dep, "pendiente") == "completado" for dep in deps):
                listos.append(paso)
    return listos
