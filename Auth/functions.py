from rest_framework.authtoken.models import Token

def get_admin_by_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        admin = token.user
        return admin
    except Token.DoesNotExist:
        return None