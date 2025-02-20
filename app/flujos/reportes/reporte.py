"""
app/flujos/reportes/Reporte.py
Modelo SQLAlchemy para la gestión de Reportes en BD.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reporte(db.Model):
    __tablename__ = 'reportes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # Ej: pendiente, en_progreso, completado

    def __repr__(self):
        return f"<Reporte {self.id} - {self.nombre} ({self.estado})>"
