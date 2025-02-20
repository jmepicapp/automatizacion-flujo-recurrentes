"""
app/api.py
API Flask para la creación de flujos a partir de recipe.yml,
almacenando cada paso en la BD.
"""

import os
import yaml
from flask import Blueprint, Flask, request, jsonify
from app import create_app, db
from app.models import Flujo

api_bp = Blueprint("api", __name__, url_prefix="/api")


def cargar_recipe(nombre_carpeta):
    """
    Carga la definición de un flujo desde app/flujos/<nombre_carpeta>/recipe.yml
    """
    ruta_recipe = f"app/flujos/{nombre_carpeta}/recipe.yml"
    with open(ruta_recipe, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@api_bp.route("/flujos", methods=["POST"])
def crear_flujo():
    """
    Crea varios registros en la BD, uno por cada paso definido en recipe.yml.
    Espera un JSON:
    {
      "carpeta_flujo": "reportes",    // nombre de la carpeta (reportes, facturacion, etc.)
      "cuerpo_global": { ... }        // parámetros globales opcionales
    }
    """
    data = request.json or {}
    carpeta_flujo = data.get("carpeta_flujo")
    cuerpo_global = data.get("cuerpo_global", {})

    if not carpeta_flujo:
        return jsonify({"error": "Falta 'carpeta_flujo'"}), 400

    recipe = cargar_recipe(carpeta_flujo)

    nombre_flujo = recipe["flujo"]["nombre"]
    pasos = recipe["flujo"]["pasos"]

    # Creamos un mapeo { nombre_paso: uuid_flujo } para asignar dependencias
    uuid_map = {}

    # Primero creamos todos los pasos en estado Pendiente
    for paso_def in pasos:
        nombre_paso = paso_def["nombre"]
        comando = paso_def["comando"]
        dependencias = paso_def.get("dependencias", [])

        # Creamos el registro del paso
        nuevo_paso = Flujo(
            nombre_flujo=nombre_flujo,
            nombre_paso=nombre_paso,
            comando=comando,
            cuerpo=cuerpo_global,  # Los parámetros globales se guardan aquí
            estado="Pendiente",
        )
        db.session.add(nuevo_paso)
        db.session.commit()

        # Guardamos en el map
        uuid_map[nombre_paso] = nuevo_paso.uuid_flujo

    # Segundo, actualizamos la columna uuid_dependencia para cada paso
    for paso_def in pasos:
        nombre_paso = paso_def["nombre"]
        dependencias = paso_def.get("dependencias", [])

        if dependencias:
            # Buscamos el registro de este paso
            paso_obj = Flujo.query.filter_by(nombre_flujo=nombre_flujo, nombre_paso=nombre_paso).first()
            # Si hay más de una dependencia, tomamos la primera para ejemplificar
            # (Podrías ampliar esto a un modelo multi-dependencia)
            primera_dependencia = dependencias[0]
            if primera_dependencia in uuid_map:
                paso_obj.uuid_dependencia = uuid_map[primera_dependencia]
                db.session.commit()

    return jsonify({
        "mensaje": f"Flujo '{nombre_flujo}' creado con {len(pasos)} pasos.",
        "pasos_creados": len(pasos),
        "uuid_pasos": uuid_map
    }), 201


def create_api_app():
    """
    Crea la app con este Blueprint y la retorna.
    """
    app = create_app()
    app.register_blueprint(api_bp)
    return app


if __name__ == "__main__":
    """
    Permite ejecutar la API con `python api.py`.
    """
    app = create_api_app()
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))
