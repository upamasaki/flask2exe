"""
This script runs the flask2exe application using a development server.
"""

from os import environ
from flask2exe import app
import webbrowser

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5050'))
    except ValueError:
        PORT = 5555

    FLASK_URL = "http://localhost:{}/".format(PORT)
    print("FLASK_URL:{}".format(FLASK_URL))
    print("HOST:{}".format(HOST))
    webbrowser.open(FLASK_URL)

    app.run(HOST, PORT, debug=True)
    

