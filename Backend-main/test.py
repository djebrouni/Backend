from django.contrib.auth.models import User
user = User.objects.get(id=1)
print(user)
