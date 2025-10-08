from typing import Union
from fastapi import FastAPI
from Model.Users import User

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register_user(username: User.username, email: User.email, password: User.password):
    try:
        if username and email and password:
            User.create_user(username, email, password)
            return {"message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/login")
def login_user(username: User.username, password: User.password):
    try:
        if username and password:
            if User.connect(password, username):
                return {"message": "Login successful"}
            else:
                return {"message": "Invalid credentials"}
    except Exception as e:
        return {"error": str(e)}