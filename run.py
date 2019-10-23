from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@localhost:5432/cadastro_usuario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)


import views, models, resources

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypet_token):
    jti = decrypet_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')