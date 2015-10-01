from app import application
from app.resources import api
from app import views
api.init_app(application)