from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from datetime import datetime
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self , email , firstname , lastname , gender , date_of_birth, phone_number ,password=None) :   #phone = None 
        """
        Creates and saves a User with the given email, 
        data of birth and password
        """
        if not email: 
            raise ValueError('User must have an email address')
        
        user = self.model(
            email = self.normalize_email(email),
            date_of_birth = date_of_birth,
            firstname = firstname , 
            lastname = lastname,
            gender= gender,
            phone_number = phone_number 
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()
    


    def create_superuser(self , email ,password=None):   #phone  firstname ,lastname , gender , phone_number, date_of_birth , 
        """
        Creates and saves a superuser with the given email, birthdat
        and password.
        """
        
        user = self.create_user(
            email=email,
            password=password,
            date_of_birth="2000-3-3",
            firstname = "admin" , 
            lastname = "adminzadeh",
            gender= 'B',
            phone_number="+989999999999" 
        )

        user.is_admin = True 
        user.is_superuser = True
        user.is_email_verified = True
        user.is_active = True
        user.role = User.TYPE_ADMIN
        user.save(using=self._db)
        return user
    

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)

    def get_by_natural_key(self, email):
        return self.get(email=email)



class User(AbstractBaseUser):
    GENDER_Male = 'M'
    GENDER_Female = 'F'
    GENDER_BOTH = 'B'
    GENDER_CHOICES = [
        (GENDER_Female, 'Female'),
        (GENDER_Male, 'Male'),
        (GENDER_BOTH , 'Both')
    ]

    TYPE_USER = "user"
    TYPE_DOCTOR = "doctor"
    TYPE_ADMIN = "admin"

    CHOICES = (
        (TYPE_USER , "User") , 
        (TYPE_DOCTOR , "Doctor") , 
        (TYPE_ADMIN , "Admin")
    )

    firstname = models.CharField(max_length=20 , blank=True, null = True )
    lastname = models.CharField(max_length=30 , blank=True, null = True )
    email = models.EmailField(
        max_length= 255 , 
        unique = True,
    )
    USERNAME_FIELD = 'email'
    
    objects = UserManager()
    date_of_birth= models.DateField(blank=True , null = True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES ,null=True ) #  default = GENDER_BOTH,
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    phone_number_regex = r'^(?:\+98|0)(?:\s?)9[0-9]{9}$'
    phone_number_validator = RegexValidator(
        regex=phone_number_regex,
        message="Phone number must be in a valid Iranian format."
    )

    phone_number = models.CharField(
        max_length=15,  # Adjust the length as per your requirement
        validators=[phone_number_validator],
        blank=True,
        null=True
    )
    role = models.CharField( max_length=255, choices=CHOICES , default=TYPE_USER)
    
    # email varification 
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    verification_tries_count = models.IntegerField(default=0)
    last_verification_sent = models.DateTimeField(null=True, blank=True, default=datetime.now())
    has_verification_tries_reset = models.BooleanField(default=False)
    
    def get_role(self ) : 
        return self.role
    
    def __str__(self):
        return self.email

    def has_perm(self , perm , obj=None ):
        "Does the user have a specific permisision?"
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    
    # profile = GenericRelation(to=Profile, related_query_name='user')

    # def get_default_profile_image(self):
    #     if self.gender == 'M':
    #         return 'images/profile_pics/male_default.png'
    #     else:
    #         return 'images/profile_pics/female_default.png'

# class Role(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
#     role = models.CharField(max_length=255, choices=User.CHOICES, default=User.TYPE_USER)