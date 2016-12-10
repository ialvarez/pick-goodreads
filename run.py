from flask import Flask
from config import DEBUG
from goodreads.app import app as goodreads_app
from instance.config import SECRET_KEY

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.register_blueprint(goodreads_app)

if __name__ == "__main__":
    app.run(port=65011)
