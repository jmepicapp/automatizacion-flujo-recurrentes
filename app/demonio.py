"""
app/demonio.py
Orquesta la ejecución de los pasos en base a sus dependencias y estados.
"""

import time
from datetime import datetime
from app import create_app, db
from app.models import Flujo


def demonio_loop():
    """
    Revisa registros en estado 'Pendiente' y ejecuta
    aquellos cuyas dependencias estén finalizadas.
    """
    app = create_app()
    with app.app_context():
        while True:
            print("Demonio: Revisando pasos Pendientes...")

            pendientes = Flujo.query.filter_by(estado="Pendiente").all()

            for paso in pendientes:
                if paso.uuid_dependencia:
                    dep = Flujo.query.filter_by(uuid_flujo=paso.uuid_dependencia).first()
                    # Si no está finalizada la dependencia, se omite
                    if not dep or dep.estado != "Finalizada":
                        continue

                # Dependencia nula o finalizada -> Se ejecuta
                ejecutar_paso(paso)

            print("Demonio: Ciclo completado. Esperando 5 segundos...\n")
            time.sleep(5)


def ejecutar_paso(paso: Flujo):
    """
    Marca un paso como En curso, simula la ejecución y lo finaliza
    (o pone en Error) al acabar.
    """
    print(f"Iniciando paso '{paso.nombre_paso}' del flujo '{paso.nombre_flujo}'...")
    paso.estado = "En curso"
    paso.fecha_estado = datetime.utcnow()
    db.session.commit()

    try:
        # Simulación de ejecución real
        time.sleep(2)
        paso.estado = "Finalizada"
        print(f"Paso '{paso.nombre_paso}' finalizado con éxito.")
    except Exception as e:
        paso.estado = "Error"
        print(f"Paso '{paso.nombre_paso}' terminó con error: {str(e)}")

    paso.fecha_estado = datetime.utcnow()
    db.session.commit()


if __name__ == "__main__":
    demonio_loop()
