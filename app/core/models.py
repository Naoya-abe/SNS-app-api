from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.id)+str(instance.displayName)+str('.')+str(ext)])


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, displayName, password=None):
        """Creats and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            displayName=displayName,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, displayName, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, displayName, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=50, unique=True)
    displayName = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_path)
    about = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['displayName']

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    """Database model for friend requests in the system"""
    askFrom = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='askFrom',
        on_delete=models.CASCADE
    )
    askTo = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='askTo',
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (('askFrom', 'askTo'),)

    def __str__(self):
        return str(self.askFrom) + '------->' + str(self.askTo)


class Message(models.Model):
    """Database model for messages in the system"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver',
        on_delete=models.CASCADE
    )
    message = models.CharField(max_length=140)

    def __str__(self):
        return str(self.sender) + '------>' + str(self.receiver)


class Post(models.Model):
    """Database model for posts in the system"""
    postFrom = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='postFrom',
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=140)

    def __str__(self):
        return str(self.postFrom) + '：' + self.content
