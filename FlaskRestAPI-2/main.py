import os

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

names = {
    "volkan": {"age": 42, "gender": "male"},
    "elif": {"age": 36, "gender": "female"},
    "talha": {"age": 12, "gender": "male"},
}


class GetNames(Resource):
    def get(self, name):
        # return {"name":name}
        return names[name]

    def post(self):
        return {"data": "you posted content"}


# api.add_resource(HelloWorld,"/helloworld")
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")
api.add_resource(GetNames, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
