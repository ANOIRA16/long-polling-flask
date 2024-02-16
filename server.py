from flask import Flask, jsonify, request
import time
import logging
from datetime import datetime, timedelta
from retrying import retry
from flask_swagger_ui import get_swaggerui_blueprint

# logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.json'  
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Notification Server API"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Retry decorator with exponential backoff
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=90000)
def get_updates():
    # This function is not needed since the S2S component directly updates the server
    pass

@app.route('/poll')
def poll():
    start_time = datetime.now()
    logging.info('Received a poll request at {}'.format(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(1)  

    while (datetime.now() - start_time).total_seconds() < 120:
        try:
            # Simulate checking for updates from the S2S component
            # This is where you would handle the updates directly without making a request
            has_update = False  # Set to True if there is an update, otherwise set to False
            message = "Update from S2S component" if has_update else "No updates."

            # logging.info('Sending response: {}'.format(message))
            logging.warning('Timeout reached. No updates received in 90 seconds.')
            
            return jsonify({"hasUpdate": has_update, "message": message})
        except Exception as e:
            logging.error('Error: {}'.format(e))
            time.sleep(10)  #wait before resending

    return jsonify({"hasUpdate": False, "message": "Timeout reached. No updates received in 90 seconds."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
