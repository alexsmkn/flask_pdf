from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Settings

app = Flask(__name__)
app.config.from_object(Settings)

db = SQLAlchemy(app)

import routes
import models

if __name__ == '__main__':
    app.run()
