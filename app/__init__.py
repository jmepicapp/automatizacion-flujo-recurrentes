"""
app/__init__.py
Inicializa la aplicación Flask y define funciones de ayuda,
como la carga de recipe.yml para cada flujo.

En esta versión, la base de datos se inicializa automáticamente al levantar la aplicación.
"""

import os
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
    Crea una instancia de la aplicación Flask con su configuración
    y crea la base de datos al arrancar.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///flujos.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Inicializa la BD al levantar la aplicación
    with app.app_context():
        db.create_all()

    return app


def cargar_recipe(nombre_flujo: str):
    """
    Carga la definición de un flujo desde su archivo YAML
    ubicado en app/flujos/<nombre_flujo>/recipe.yml.
    """
    ruta_recipe = f"flujos/{nombre_flujo}/recipe.yml"
    with open(ruta_recipe, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
