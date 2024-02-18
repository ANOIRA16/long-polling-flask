import requests
import logging
import json
import time
from flask import Flask
from flask_restx import Api, Resource, fields

logging.basicConfig(level=logging.INFO)

app = Flask(__name__) 
api = Api(app, version='1.0', title='S2S Server API',
          description='Server-to-Server Communication for sending updates')

ns = api.namespace('/', description='Send updates')

update_model = api.model('Update', {
    'message': fields.String(required=True, description='The update message')
})

def send_update_to_main_server():
    main_server_url = "http://localhost:5000/update/"
    # Example fake data update
    fake_data = {"message": "This is a fake update sent at " + time.strftime("%Y-%m-%d %H:%M:%S")}
    try:
        response = requests.post(main_server_url, json=fake_data)
        if response.status_code == 200:
            logging.info("Successfully sent update to the main server. Data: " + json.dumps(fake_data))
        else:
            logging.error("Failed to send update to the main server. Status Code: " + str(response.status_code))
    except Exception as e:
        logging.error("Error sending update to the main server: " + str(e))

@ns.route('/send-update')
class SendUpdate(Resource):
    @api.expect(update_model)
    def post(self):
        """Trigger an update to the main server."""
        send_update_to_main_server()
        return {"message": "Triggered update to main server"}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)

# Automatically sending updates every 30 seconds for demonstration
# def auto_send_updates():
#     while True:
#         send_update_to_main_server()
#         time.sleep(200)

# Starting the automatic updates in a separate thread to avoid blocking
# from threading import Thread
# update_thread = Thread(target=auto_send_updates)
# update_thread.start()
