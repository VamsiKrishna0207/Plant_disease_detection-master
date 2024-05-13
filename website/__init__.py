from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import numpy as np
from keras.preprocessing import image
from PIL import Image
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
# import cv2
from base64 import b64encode
from keras.models import load_model

db = SQLAlchemy()
DB_NAME = "database.db"

def Res(a):
    image = b64encode(a).decode("utf-8")
    return image

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.jinja_env.globals.update(Res=Res)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, History
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
def load_image(image_file):
	img = Image.open(image_file)
	return img
# Function to check the image
# @st.cache(ttl=48*3600)
def check():

    lr = load_model('weights.hdf5')
    #Prediction Pipeline
    class Preprocessor(BaseEstimator, TransformerMixin):
        def fit(self,img_object):
            return self
        
        def transform(self,img_object):
            img_array = image.img_to_array(img_object)
            expanded = (np.expand_dims(img_array,axis=0))
            return expanded

    class Predictor(BaseEstimator, TransformerMixin):
        def fit(self,img_array):
            return self
        
        def predict(self,img_array):
            probabilities = lr.predict(img_array)
            predicted_class = ['Phosphorus Deficiency', 'Healthy', 'Nitrogen Deficiency', 'Potassium Deficiency'][probabilities.argmax()]
            return predicted_class

    full_pipeline = Pipeline([('preprocessor',Preprocessor()),
                            ('predictor',Predictor())])
    return full_pipeline

def output(full_pipeline,img):
   a=  img
   #a = img.decode('utf-8', 'ignore') 
   a= a.resize((224,224))
   predic = full_pipeline.predict(a)
   return(predic)


