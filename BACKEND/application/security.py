from flask_jwt_extended import JWTManager
from application.models import User

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)   # ✅ Must be string

@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(int(identity))   # ✅ Convert back to int before querying
