from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with either
    their username or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        if username is None or password is None:
            return None
        
        # Try to fetch the user by searching the username or email field
        user = None
        
        # Try username first
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Try email - use filter().first() to avoid MultipleObjectsReturned
            user = User.objects.filter(email=username).first()
            if not user:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user
                User().set_password(password)
                return None
        
        # Check the password
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
