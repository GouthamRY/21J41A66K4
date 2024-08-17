import requests0
from collections import deque
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Configuration
WINDOW_SIZE = 10
TEST_SERVER_URL = "http://your_test_server/numbers/{numberId}"
TIMEOUT = 500

# In-memory storage for numbers (can be replaced with a database for persistence)
number_window = deque(maxlen=WINDOW_SIZE)

class AverageCalculator(Resource):
    def get(self, numberId):
        try:
            # Fetch numbers from test server
            response = requests.get(TEST_SERVER_URL.format(numberId=numberId), timeout=TIMEOUT)
            if response.status_code != 200:
                return {"error": "Failed to fetch numbers"}, 500

            numbers = response.json()["numbers"]

            # Update number window
            for num in numbers:
                if num not in number_window:
                    number_window.append(num)

            # Calculate average
            average = sum(number_window) / len(number_window)

            return {
                "numbers": numbers,
                "windowPrevState": list(number_window)[:-len(numbers)],
                "windowCurrState": list(number_window),
                "avg": average
            }

        except requests.exceptions.Timeout:
            # Handle timeout
            return {"error": "Test server timeout"}, 500
        except Exception as e:
            # Handle other errors
            return {"error": str(e)}, 500

api.add_resource(AverageCalculator, '/numbers/<string:numberId>')

if __name__ == '__main__':
    app.run(debug=True)