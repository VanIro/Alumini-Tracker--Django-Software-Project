from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.hashers import make_password


# Create your models here.
class sentinel:
    counter=-1
    @staticmethod
    def get_sentinel_user(self):
        sentinel.counter+=1
        return get_user_model.objects.get_or_create(groups__name="deleted", username=f'deleted{sentinel.counter}')

def validate_group(username):
    useru = User.objects.get(id=username)
    if not useru.groups.filter(name="Institutes").exists():
        raise ValidationError(
            (f'{useru.username} was not found to be a member of "Institutes".')
        )

TITLE_CHOICES = (
    ("Dr.", "Dr."),
    ("Er.", "Er."),
    ("Mr.", "Mr."),
    ("Ms.", "Ms."),
    ("Mrs.", "Mrs."),
)
class Institute(models.Model):
    title = models.CharField(
        max_length=10,
        choices=TITLE_CHOICES,
        blank=True, null=True,
    )
    first_name = models.CharField(max_length=200, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)

    userName = models.OneToOneField(User,
        on_delete=models.SET(sentinel.get_sentinel_user)
        ,validators=[validate_group], 
        blank=False, null=False, 
        related_name="institute"
    )

    id_code = models.CharField(max_length=15, blank=False, null=False)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    recent_passport_size_photo = models.FileField(
        upload_to="documents_photos/",
        blank=True,
        null=True,
    )

    position_in_institution = models.CharField(
        blank=True, 
        null=True, 
        max_length=100
    )
    date_of_enrollment = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(r'^20[0-9][0-9]/[0-9]{2}/[0-9]{2}$'), 
            MaxLengthValidator(10), MinLengthValidator(10)
        ], 
        blank=True, 
        null=True
    )

    def __str__(self):
        full_name=self.first_name
        if self.middle_name:
            full_name+= " " + self.middle_name
        full_name+=f' {self.last_name}'
        return full_name

    @property
    def full_name(self):
        return self.__str__()
    #def save(self, **kwargs):
    #
    #    super().save(**kwargs)