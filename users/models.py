from django.db import models
from django.core import validators
from django.utils import six, timezone
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.core.mail import send_mail

class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        ('username'),
        max_length=30,
        unique=False,
        help_text=('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    email = models.EmailField(('email address'), unique=True, validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Enter a valid email. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': ("A user with that email already exists."),
        },)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    phone    = models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




class MyUser(BaseUser):
    def __str__(self):
        return self.email
