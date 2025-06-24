# mixins.py
from rest_framework.response import Response
from rest_framework import status
from login.utils import verify_jwt  # Adjust path as needed

class GetUserFromTokenMixin:
    """A mixin for extracting user information from a JWT token."""

    def get_user_from_token(self, token):
        """Returns user object or an error Response."""
        from user.models import CustomUser
        payload = verify_jwt(token)
        if not payload:
            return None, Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)  # or AdminUser
            return user, None
        except CustomUser.DoesNotExist:
            return None, Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
