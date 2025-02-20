"""
tests/test_api.py
Pruebas unitarias para la API.
Puedes usar pytest o unittest. Aquí un ejemplo simple con unittest.
"""

import unittest

from app.api import create_api_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_api_app()
        self.client = self.app.test_client()

    def test_crear_flujo_sin_parametros(self):
        response = self.client.post("/flujos", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Debe especificar un flujo", response.data)

    def test_crear_flujo_reportes(self):
        response = self.client.post("/flujos", json={"flujo": "reportes"})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Generaci", response.data)  # Checking for partial text


if __name__ == "__main__":
    unittest.main()

reportes_body_example = {
    "carpeta_flujo": "",
    "cuerpo_global": {
        "fecha": "20/02/2025",
        "cantidad_paginas": "5",
        "resumen": "Resumen del informe generado"
    }
}

facturacion_body_example = {
    "carpeta_flujo": "",
    "cuerpo_global": {
        "fecha": "20/02/2025",
        "email_cliente": "jmaguero@profile.es",
        "factura_id": 123456,
        "nombre_cliente": "Profile",
        "cantidad_total": 5000
    }
}
