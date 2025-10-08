import bcrypt
import re

class User:
    def __init__(self, user_id, username, email, password_hash, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.password = password
    
    def hash_pass(self, password):
        try:
            if password is not None:
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        except Exception as e:
            print(f"Error hashing password: {e}")
        return hash, salt
    
    def verify_pass(self, password, stored_hash):
        try:
            if not password or not stored_hash:
                return False
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

    def create_user(self, username, email, password):
        try:
            if username is not None and email is not None and password is not None:
                password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                hash, salt = self.hash_pass(password)
                self.username = username
                self.email = email
                if password is not None and re.match(password_regex, password):
                    self.password = password
                    self.password_hash = hash
                return hash, salt
        except Exception as e:
            print(f"Error creating user: {e}")
    
    def connect(self, password, username):
        is_connected = False
        try:
            if password is not None and username is not None and self.password_hash is not None:
                if self.verify_pass(password, self.password_hash) == True:
                    is_connected = True
                return is_connected
            else:
                return False
        except Exception as e:
            print(f"Error connecting user: {e}")
        return False