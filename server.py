from server_core import create_app
from flask import jsonify
from api.visit_info import add_visit_info

app = create_app()


@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({
        "code": 500,
        "message": f"{type(e).__name__}: {e}"
    })
    response.status_code = 500
    return response

@app.before_request
def handle_request():
    add_visit_info()

@app.after_request
def handle_response(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
