import os

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

names = {
    "volkan": {"age": 42, "gender": "male"},
    "elif": {"age": 36, "gender": "female"}
}


class HelloWorld(Resource):
    def get(self, name):
        # return {"name":name}
        return names[name]

    def post(self):
        return {"data": "you posted content"}


def idNotFound(id):
    if id not in videos:
        abort(404, "Given id doesnt find in videos !!!")


def idAlreadyExist(id):
    if id in videos:
        abort(409, "Given id is already exist in videos")


video_put_arg = reqparse.RequestParser()
video_put_arg.add_argument("name", type=str, help="Name of the Video Required", required=True)
video_put_arg.add_argument("views", type=int, help="Views of the Video Required", required=True)
video_put_arg.add_argument("likes", type=int, help="Likes of the Video Required", required=True)

videos = {1: {"name": "deneme"}}


class Video(Resource):
    def get(self, id):
        idNotFound(id)
        return videos[id]

    def put(self, id):
        idAlreadyExist(id)
        args = video_put_arg.parse_args()
        videos[id] = args
        return videos[id], 201

    def delete(self, id):
        idNotFound(id)
        del videos[id]
        return "", 204


# api.add_resource(HelloWorld,"/helloworld")
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
