from .models import Token

def get_user_by_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        admin = token.user
        return admin
    except Token.DoesNotExist:
        return None