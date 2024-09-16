import os

class Config:
    SECRET_KEY = os.urandom(24)  # Isso gera uma chave aleatória cada vez que a aplicação é iniciada
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rodri0502@localhost/hospital'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
