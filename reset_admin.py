from django.contrib.auth import get_user_model
User = get_user_model()
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print("Password reset to: admin123")
except User.DoesNotExist:
    print("Admin user does not exist")
