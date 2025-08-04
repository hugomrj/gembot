# run.py
from app.main import app
import bottle

if __name__ == '__main__':
    bottle.run(app=app, host='localhost', port=3000, debug=True, reloader=True)

