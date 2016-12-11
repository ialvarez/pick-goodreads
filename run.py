from flask import Flask
from flask_bootstrap import Bootstrap
from config import DEBUG
from goodreads.app import app as goodreads_app
from instance.config import SECRET_KEY

app = Flask(__name__)
Bootstrap(app)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.register_blueprint(goodreads_app)
app.config.update({'TEMPLATES_AUTO_RELOAD': True})

if __name__ == "__main__":
    app.run(port=65011)
