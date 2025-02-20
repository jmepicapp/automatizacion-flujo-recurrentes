"""
app/models.py
Define el modelo Flujo, que representa cada 'paso' de un flujo en la base de datos.
"""

import uuid
from datetime import datetime
from app import db


class Flujo(db.Model):
    """
    Representa un paso/tarea de un flujo en la BD.
    - uuid_flujo: identificador único (string)
    - nombre_flujo: nombre global del flujo
    - nombre_paso: nombre del paso concreto
    - comando: comando o acción del paso (opcional)
    - cuerpo: parámetros de la llamada (JSON)
    - estado: Pendiente, En curso, Finalizada, Error
    - uuid_dependencia: uuid_flujo de otro paso que debe estar finalizado antes
    - fecha_alta: fecha de creación
    - fecha_estado: fecha de última modificación del estado
    """
    __tablename__ = "flujos"

    id = db.Column(db.Integer, primary_key=True)
    uuid_flujo = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    nombre_flujo = db.Column(db.String(100), nullable=False)  # Nombre global del flujo (p. ej. "Reportes")
    nombre_paso = db.Column(db.String(100), nullable=False)  # Nombre específico del paso (p. ej. "Validación de Datos")
    comando = db.Column(db.String(100), nullable=True)

    cuerpo = db.Column(db.JSON, nullable=True)

    estado = db.Column(db.String(20), default="Pendiente")  # Pendiente, En curso, Finalizada, Error
    uuid_dependencia = db.Column(db.String(36), nullable=True)

    fecha_alta = db.Column(db.DateTime, default=datetime.now())
    fecha_estado = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"<Flujo {self.uuid_flujo} - {self.nombre_flujo}/{self.nombre_paso} ({self.estado})>"
