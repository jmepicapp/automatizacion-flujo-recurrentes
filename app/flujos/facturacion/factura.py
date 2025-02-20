"""
app/flujos/facturacion/Factura.py
Modelo SQLAlchemy para la gestión de Facturas en BD.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="pendiente")  # pendiente, generada, enviada

    def __repr__(self):
        return f"<Factura {self.id} - {self.cliente} ({self.estado})>"
