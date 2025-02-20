"""
app/demonio.py
Orquesta la ejecución de los pasos en base a sus dependencias y estados.
"""
import os
import time
from datetime import datetime
from app import create_app, db
from flujo_model import Flujo


def demonio_loop():
    """
    Revisa registros en estado 'Pendiente' y ejecuta
    aquellos cuyas dependencias estén 'Finalizada'.
    """
    app = create_app()
    with app.app_context():
        while True:
            print("Demonio: Revisando pasos en estado 'Pendiente'...")

            # Buscar todos los pasos pendientes
            pendientes = Flujo.query.filter_by(estado="Pendiente").all()

            for paso in pendientes:
                # Si existe una dependencia, comprobamos si ya está finalizada
                if paso.uuid_dependencia:
                    paso_dependencia = Flujo.query.filter_by(uuid_flujo=paso.uuid_dependencia).first()
                    if not paso_dependencia or paso_dependencia.estado != "Finalizada":
                        # Si la dependencia no existe o no está finalizada, no se ejecuta
                        continue

                # Si no tiene dependencia o la dependencia está finalizada, se ejecuta
                ejecutar_paso(paso)

            print("Demonio: Ciclo completado. Esperando 5 segundos...\n")
            time.sleep(5)

def ejecutar_paso(paso: Flujo):
    """
    Marca el paso como 'En curso', simula su ejecución y
    lo pasa a 'Finalizada' o 'Error' al acabar.
    """
    print(f"""
    ------------------------------------------------------------------------------
    Iniciando paso '{paso.nombre_paso}' del flujo '{paso.nombre_flujo}'...""")
    paso.estado = "En curso"
    paso.fecha_estado = datetime.now()
    db.session.commit()

    try:
        # Simula el trabajo real que pueda ocasionar una excepción
        time.sleep(2)
        paso.estado = "Finalizada"
        print(f"""
        ------------------------------------------------------------------------------
        Paso '{paso.nombre_paso}' finalizado con éxito.""")

    except Exception as e:
        paso.estado = "Error"
        print(f"Paso '{paso.nombre_paso}' terminó con error: {str(e)}")

    paso.fecha_estado = datetime.now()
    db.session.commit()

if __name__ == "__main__":
    demonio_loop()
