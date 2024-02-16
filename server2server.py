from flask import Flask, request
from flask_restx import Api, Resource, fields
import logging
import requests
import json
import random

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app, version='1.0', title='Server-to-Server API',
          description='Manage updates between servers')

# Namespace declaration
ns = api.namespace('updates', description='Update operations')

# Model for the update (for Swagger documentation)
update_model = api.model('Update', {
    'message': fields.String(required=True, description='Update message')
})

# Simulated storage for updates
updates = []

@ns.route('/post-update')
class PostUpdate(Resource):
    @api.expect(update_model)
    def post(self):
        """Post an update from Kafka"""
        received_update = api.payload['message']
        updates.append(received_update)

        # Send a random update to the main server
        random_update = random.choice(updates) if updates else "No updates available"
        send_update_to_main_server(random_update)

        return {"message": "Update received and sent to main server"}, 201

def send_update_to_main_server(update):
    main_server_url = "http://localhost:5000/poll"  # Replace with your main server URL
    payload = {"message": update}
    headers = {"Content-Type": "application/json"}
    requests.post(main_server_url, data=json.dumps(payload), headers=headers)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
