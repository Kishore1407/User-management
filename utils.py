from itsdangerous import URLSafeSerializer

SECRET_KEY = "your-very-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

# Create a secure token
def create_session_token(username: str) -> str:
    return serializer.dumps({"username": username})

# Verify the token
def verify_session_token(token: str) -> bool:
    try:
        data = serializer.loads(token)
        return "username" in data  # optionally: check for specific users
    except Exception:
        return False
def get_username_from_token(token: str) -> str | None:
    try:
        data = serializer.loads(token)
        return data.get("username")
    except Exception:
        return None