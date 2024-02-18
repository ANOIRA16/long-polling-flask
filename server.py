from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app, version='1.0', title='NOTIFICATION Server API',
          description='Main Server for receiving updates and serving them to clients')

ns = api.namespace('update', description='Update operations')

update_model = api.model('Update', {
    'message': fields.String(required=True, description='The update message')
})

table_state = {"message": "Initial state", "hasUpdate": False}

@ns.route('/')
class Update(Resource):
    @api.doc(responses={200: 'UPDATE SEND SUCCESS', 408: 'TIMEOUT, NO UPDATE'}, description="Post an update to the main notification server")
    @api.expect(update_model)
    def post(self):
        """Receives an update from S2S and updates the table state."""
        global table_state
        table_state['message'] = api.payload['message']
        
        table_state['hasUpdate'] = False
        
        logging.info(f"Table updated with: {table_state['message']}")
        return {"message": "Table updated successfully"}, 200

@ns.route('/poll')
class Poll(Resource):
    @api.doc(description="Long polls for updates to the table")
    def get(self):
        """Long polls for updates and returns them to the client."""
        start_time = datetime.now()
        logging.info(f'Received a poll request at {start_time.strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Simulate the waiting period for demonstration purposes
        wait_time_seconds = 180  # Define your wait time (180 seconds as per your setup)
        while (datetime.now() - start_time).total_seconds() < wait_time_seconds:
            if table_state["hasUpdate"]:
                # If somehow hasUpdate becomes True, prepare to break the loop
                break
            # Implement a sleep here if you're checking for updates in a loop to avoid high CPU usage
            # Example: time.sleep(1)
        
        logging.info(f'Responding to poll request at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} after waiting or due to an update.')

        # Reset the hasUpdate flag and respond to the poll request
        response = jsonify({"hasUpdate": table_state["hasUpdate"], "message": table_state["message"]})
        table_state["hasUpdate"] = False  # Consider if this is the behavior you want
        return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
