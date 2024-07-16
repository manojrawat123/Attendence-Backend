from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from mybrand.models import Brand


def validate_date_of_birth(value):
    minimum_age = 15
    minimum_birth_date = date.today() - timedelta(days=365 * minimum_age)
    if (value > minimum_birth_date):
        raise ValidationError("Employee must atleast 15 or above")

def validate_date_of_joning(value):
    company_founded_date = date(2016,1, 1)
    if (value < company_founded_date):
        raise ValidationError("Date Of Joining should not before 2016 (#Company Founded Date)")  

class EmployeeUserManager(BaseUserManager):
    def create_user(self, email, name, password = None, password2 = None ):
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            # phone = phone
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, email, name, phone, password = None, password2 = None):
        if password == password2:
            raise ValueError("password Didn't match")
        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
# Create your models here.
class EmployeeUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name = "email address",
        max_length = 225,
        unique = True,
    )
    name = models.CharField(max_length = 225)
    phone = models.IntegerField(unique = True, null=True , blank = True)
    address = models.TextField(null=True , blank = True)
    date_of_birth = models.DateField(validators = [validate_date_of_birth],null=True, blank=True)
    date_of_joining = models.DateField(
        validators = [
            validate_date_of_joning
        ],null=True, blank=True
    )
    role = models.CharField(max_length = 225,null = True, blank = True)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=225, choices = [
        ("Intern", "Intern"),
        ("Employee", "Employee"),
        ("Senior Employee", "Senior Employee"),
        ("CEO","CEO"),
        ("Teacher", "Teacher")
    ],null=True, blank=True)
    objects = EmployeeUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]
    def __str__(self):
        return self.name
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Handle permissions here (if needed)
        return True

    def has_module_perms(self, app_label):
        # Handle module permissions here (if needed)
        return True

    @property
    def is_staff(self):
        # Use the is_superuser field provided by AbstractBaseUser
        return self.is_admin