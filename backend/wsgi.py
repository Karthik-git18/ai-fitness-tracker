import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../frontend')

# CORS is already handled by flask-cors
# This config is for production

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
