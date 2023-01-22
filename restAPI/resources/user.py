from flask_views import MethodView
from flask_smorest import Blueprint, abort
from passlib_hash import pbkdf2_sha256
## pass lib will allow us to hash passwords
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operation on users")

@blp.route("/register")
class UserRegister(MethodView):
    ##blp.arguments
    ##allow us to process the data passed with the schema
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username = user_data["username"]).first():
            abort(409, message="A user with tat username already exists.")
        user = UserModel(
            username = user_data["username"],
            ##hashing password
            password = pbkdf2._sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created succesfully"}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data);
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            ##with verify we are not unhashing the passwrod we are
            ##just verifying that the passed password hashed is equal to the 
            ##hash stored
            access_token = create_access_token(idendity=user.id)
            ## we are storing user id in the jwt
            ##ensuring that this token in only valid for the user who creates it 
            return {"access_token": access_token}
        abort(401, message="Invaid credentials.")





@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.sesion.delete(user)
        db.session.commit()
        return {"message":"User deleted."}, 200
