import logging
import time

from celery_worker import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="send_email")
def send_email(email, msg):
    try:
        logger.info(f"Enviando email a {email}")
        # logica para el envio del correo
        time.sleep(60)
    except Exception as exc:
        logger.error(exc)
        return f"Error al enviar correo a {email}"

    return f"Correo enviado a {email} con mensaje {msg}"


@celery_app.task(name="add_numbers")
def add_numbers(a, b):
    for i in range(a, b):
        logging.info(i)
    time.sleep(60)
    return {"number": a + b}


# Configurar rutas de tareas (OPCIONAL porque vamos a usar un solo worker y una sola cola)
# celery_app.conf.task_routes = {
#     'app.celery_tasks.send_email': {'queue': 'email_queue'},
#     'app.celery_tasks.add_numbers': {'queue': 'adding_queue'},
# }
