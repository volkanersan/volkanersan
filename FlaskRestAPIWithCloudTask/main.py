import os
import threading
from multiprocessing import Process

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse
import datetime
import json

from google.cloud import tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2

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


class CreateCloudTask(Resource):

    @staticmethod
    def createTask(number):
        # Create a client.
        client = tasks_v2.CloudTasksClient()

        # TODO(developer): Uncomment these lines and replace with your values.
        project = 'test-project-intra'
        queue = 'my-queue'
        location = 'us-central1'
        url = 'https://flasktest-kouti6u5va-uc.a.run.app/helloworld/volkan'
        # TODO for application/json
        payload = ''  # or {'param': 'value'}

        in_seconds = 180
        task_name = f'my-test{number}-task'
        deadline = 900

        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)

        # Construct the request body.
        task = {
            "http_request": {  # Specify the type of request.
                "http_method": tasks_v2.HttpMethod.GET,
                "url": url,  # The full url path that the task will be sent to.
            }
        }
        if payload is not None:
            if isinstance(payload, dict):
                # Convert dict to JSON string
                payload = json.dumps(payload)
                # specify http content-type to application/json
                task["http_request"]["headers"] = {"Content-type": "application/json"}

            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task["http_request"]["body"] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task["schedule_time"] = timestamp

        if task_name is not None:
            # Add the name to tasks.
            task["name"] = client.task_path(project, location, queue, task_name)

        if deadline is not None:
            # Add dispatch deadline for requests sent to the worker.
            duration = duration_pb2.Duration()
            duration.FromSeconds(deadline)
            task["dispatch_deadline"] = duration

        # Use the client to build and send the task.
        response = client.create_task(request={"parent": parent, "task": task})

        print("Created task {}".format(response.name))

    process = []
    for i in range(0, 10):
        proc = Process(target=createTask, args=(i))
        process.append(proc)
        proc.start()
    for pro in process:
        pro.join()


# api.add_resource(HelloWorld,"/helloworld")
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")
api.add_resource(GetNames, "/helloworld/<string:name>")
api.add_resource(CreateCloudTask, "/createtask")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
