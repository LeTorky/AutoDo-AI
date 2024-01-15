from rest_framework.authentication import BaseAuthentication
from authlib.jose import jwt
from dotenv import load_dotenv
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

load_dotenv()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            encoded_token = self._extract_token(request)
        except (AttributeError, KeyError, NameError):
            return None

        try:
            decoded_token = self._validate_token(encoded_token)
        except AuthenticationFailed:
            return None

        user = User.objects.first()

        return (user, decoded_token)

    def _extract_token(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise KeyError('No authorization header')
        prefix, token = auth_header.split(' ')
        if prefix != 'AccessToken':
            raise NameError('Invalid token type')
        return token

    def _validate_token(self, encoded_token):
        public_key_path = os.getenv('PUBLIC_KEY_PATH')
        with open(public_key_path, "r") as file:
            public_key = file.read()
        binary_public_key = public_key.encode('ascii')
        claims = jwt.decode(
            encoded_token, binary_public_key)
        try:
            claims.validate()
        except Exception:
            raise AuthenticationFailed()
        return encoded_token
