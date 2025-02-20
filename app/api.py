"""
app/api.py
API Flask para la creación de flujos a partir de receta.yml,
almacenando cada paso en la BD. Documentada con Flask-RESTX.
"""

import os

import yaml
from flask import Blueprint
from flask_restx import Api, Resource, fields

from app import create_app, db
from flujo_model import Flujo

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    api_bp,
    version="1.0",
    title="Automatización de Flujos",
    description="API para la creación y gestión de flujos, documentada con Swagger",
)

flujos_ns = api.namespace("flujos", description="Operaciones relacionadas con la creación de flujos")

# Modelo de datos para la petición
flujo_model = api.model("FlujoRequest", {
    "carpeta_flujo": fields.String(required=True, description="Nombre de la carpeta (p.ej. 'reportes', 'facturacion')"),
    "cuerpo_global": fields.Raw(required=False, description="Parámetros globales opcionales en formato JSON")
})

def cargar_receta(nombre_carpeta):
    """
    Carga la definición de un flujo desde app/flujos/<nombre_carpeta>/receta.yml
    """
    ruta_receta = f"app/flujos/{nombre_carpeta}/receta.yml"
    with open(ruta_receta, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@flujos_ns.route("")
class CrearFlujo(Resource):
    @flujos_ns.expect(flujo_model, validate=True)
    def post(self):
        """
        Crea varios registros en la BD, uno por cada paso definido en la receta.
        """
        data = api.payload or {}
        carpeta_flujo = data.get("carpeta_flujo")
        cuerpo_global = data.get("cuerpo_global", {})

        receta = cargar_receta(carpeta_flujo)
        nombre_flujo = receta["flujo"]["nombre"]
        pasos = receta["flujo"]["pasos"]

        # Crear un mapeo para asignar dependencias
        uuid_map = {}

        # 1. Crear todos los pasos en estado Pendiente
        for paso_def in pasos:
            nombre_paso = paso_def["nombre"]
            comando = paso_def.get("comando")

            nuevo_paso = Flujo(
                nombre_flujo=nombre_flujo,
                nombre_paso=nombre_paso,
                comando=comando,
                cuerpo=cuerpo_global,
                estado="Pendiente",
            )
            db.session.add(nuevo_paso)
            db.session.commit()

            uuid_map[nombre_paso] = nuevo_paso.uuid_flujo

        # 2. Actualizar uuid_dependencia para cada paso
        for paso_def in pasos:
            nombre_paso = paso_def["nombre"]
            dependencias = paso_def.get("dependencias", [])

            if dependencias:
                paso_obj = Flujo.query.filter_by(nombre_flujo=nombre_flujo, nombre_paso=nombre_paso).first()
                # Ejemplo: si solo tomamos la primera dependencia
                primera = dependencias[0]
                paso_obj.uuid_dependencia = uuid_map[primera]
                db.session.commit()

        return {
            "mensaje": f"Flujo '{nombre_flujo}' creado con {len(pasos)} pasos.",
            "pasos_creados": len(pasos),
            "uuid_pasos": uuid_map
        }, 201

    def get(self):
        """
        Devuelve un listado de objetos, donde cada objeto representa un flujo completo (agrupado por nombre_flujo) con todos sus pasos.
        """
        # 1. Obtener todos los 'nombre_flujo' distintos
        nombre_flujos = (
            db.session.query(Flujo.nombre_flujo)
            .distinct()
            .order_by(Flujo.nombre_flujo)
            .all()
        )
        # Esto retorna una lista de tuplas, p. ej. [('Reportes',), ('Facturacion',), ...]

        resultado = []
        for (nombre,) in nombre_flujos:
            # 2. Buscar todos los pasos de ese nombre_flujo
            pasos_de_este_flujo = Flujo.query.filter_by(nombre_flujo=nombre).all()

            # 3. Construir la lista de pasos con la info necesaria
            pasos_list = []
            for p in pasos_de_este_flujo:
                pasos_list.append({
                    "uuid_flujo": p.uuid_flujo,
                    "nombre_paso": p.nombre_paso,
                    "comando": p.comando,
                    "estado": p.estado,
                    "uuid_dependencia": p.uuid_dependencia,
                    "fecha_alta": p.fecha_alta.isoformat(),
                    "fecha_estado": p.fecha_estado.isoformat()
                })

            # 4. Cada elemento del array representará UN flujo completo
            flujo_obj = {
                "nombre_flujo": nombre,
                "pasos": pasos_list
            }
            resultado.append(flujo_obj)

        # 5. Devolver la lista, donde cada elemento es un flujo completo
        return {
            "flujos": resultado,
            "total_flujos": len(resultado),
            "mensaje": "Listado agrupado por flujos con sus pasos correspondientes."
        }, 200

@flujos_ns.route("/<string:uuid_flujo>")
class FlujoDetalle(Resource):
    def get(self, uuid_flujo):
        """
        Dado el uuid_flujo de un paso, devuelve todos los pasos relacionados (mismo nombre_flujo).
        """
        # 1. Encontrar el registro en base al uuid_flujo
        registro = Flujo.query.filter_by(uuid_flujo=uuid_flujo).first()
        if not registro:
            return {"error": "No existe un registro con ese uuid_flujo"}, 404

        # 2. Buscar todos los pasos que pertenezcan al mismo nombre_flujo
        pasos_relacionados = Flujo.query.filter_by(nombre_flujo=registro.nombre_flujo).all()

        # 3. Construir la respuesta con los datos relevantes
        respuesta = []
        for paso in pasos_relacionados:
            respuesta.append({
                "uuid_flujo": paso.uuid_flujo,
                "nombre_flujo": paso.nombre_flujo,
                "nombre_paso": paso.nombre_paso,
                "estado": paso.estado,
                "uuid_dependencia": paso.uuid_dependencia,
                "fecha_alta": paso.fecha_alta.isoformat(),
                "fecha_estado": paso.fecha_estado.isoformat()
            })

        return {
            "flujo_principal": {
                "uuid_flujo": registro.uuid_flujo,
                "nombre_flujo": registro.nombre_flujo
            },
            "pasos_relacionados": respuesta
        }, 200


def create_api_app():
    """
    Crea la app, registra el blueprint con Flask-RESTX y retorna la instancia.
    """
    app = create_app()
    app.register_blueprint(api_bp)  # /api
    return app

if __name__ == "__main__":
    """
    Ejecutar la API con Swagger:
    http://127.0.0.1:5000/api
    Documentación: http://127.0.0.1:5000/api/
    """
    app = create_api_app()
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))
