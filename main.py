from flask import Flask, request, jsonify
from flask_limiter.util import get_remote_address
from gevent.pywsgi import WSGIServer
from flask_limiter import Limiter

from AuthService import AuthService
from data.DefaultTransaction import DefaultTransaction

app = Flask(__name__)

repository = DefaultTransaction()

limiter = Limiter(
    get_remote_address,  # Визначає клієнта за IP
    app=app,
)


@app.before_request
def auth():
    if request.endpoint in ['news', 'activate']:
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"result": False, "error": "Authorization header is missing"}), 401

    if not AuthService.verify_jwt(auth_header):
        return jsonify({"result": False, "error": "Authorization Token is not correct"}), 401


@app.route("/api/news", methods=["GET"])
@limiter.limit("60 per minute")
def news():
    page = int(request.args.get('page', 1))
    offset = (page - 1) * 5
    return repository.news(offset)


@app.route("/api/post", methods=["POST"])
@limiter.limit("1 per minute")
def post():
    data = request.get_json()

    if not data.get("title", None) or not data.get("desc", None) or not data.get("img_data", None):
        return jsonify({"result": False, "error": "Lose some params of (`title`, `desc` or `img_data`)"}), 400

    return repository.post(data['title'], data['desc'], data['img_data'])


@app.route("/api/delete", methods=["DELETE"])
@limiter.limit("1 per minute")
def delete():
    data = request.get_json()

    if not data.get("identify", None):
        return jsonify({"result": False, "error": "Lose param (`identify`)"}), 400

    return repository.remove(data['identify'])


@app.route("/api/activate", methods=["POST"])
@limiter.limit("1 per minute")
def activate():
    data = request.get_json()

    if not data.get('uuid', None) or not data.get('android_id', None):
        return jsonify({"result": False, "error": "Lose some params of (`uuid` or `android_id`)"}), 400

    return repository.register_auth(data['uuid'], data['android_id'])


if __name__ == '__main__':
    app.run(threaded=True)
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()