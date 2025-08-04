from app import app

application = app  # necesario para WSGI




# Un servidor WSGI como Gunicorn buscará la variable 'application' por defecto.
# Ejemplo de cómo ejecutarlo con Gunicorn:
# gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:application
