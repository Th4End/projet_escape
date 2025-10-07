import bcrypt

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
            is_valid = False
            if password is not None and stored_hash is not None:
                is_valid = True
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            print(f"Error verifying password: {e}")
        return is_valid

    def create_paswd(self, password):
        try:
            if password is not None:
                hash, salt = self.hash_pass(password)
                self.password_hash = hash
                self.password = password
                return hash, salt
        except Exception as e:
            print(f"Error creating password: {e}")