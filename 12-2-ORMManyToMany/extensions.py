from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# This is the recommended pattern to create a db object that can be reference both 
# by the app and by models.py without creating any circular references