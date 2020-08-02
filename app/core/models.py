from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.userPro.id)+str(instance.displayName)+str('.')+str(ext)])


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creats and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):

    displayName = models.CharField(max_length=20, unique=True)
    userPro = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userPro', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_path)
    about = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.displayName


class FriendRequest(models.Model):
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
        return str(self.sender)


class Post(models.Model):
    postFrom = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='postFrom',
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.postFrom
