from datetime import timedelta

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/flask_jwt"
SQLALCHEMY_TRACK_MODIFICATIONS = True
jwt_config = {
    'JWT_SECRET_KEY': 'jwt_secret',
    'JWT_AUTH_URL_RULE': '/api/v1/auth',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=120)
}