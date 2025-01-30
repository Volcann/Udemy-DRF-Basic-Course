from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


#BaseUserManager is the parent class
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #default password is none
    def create_user(self, email, name, password=None):
         """Create a new user profile"""
         if not email:
             raise ValueError('User must have an email address.')

        # makes first half of email as case sensitive while second half of email is not case sensitive
         email=self.normalize_email(email)
         user=self.model(email=email, name=name)

         #sets hashed password in db
         user.set_password(password)
         user.save(using=self._db)

         return user

    def create_superuser(self, email, name, password):
         """Create and save a new superuser with given details"""
         user= self.create_user(email, name, password)

#is_superuser is automatically created by PermissionsMixin
         user.is_superuser= True
         user.is_staff=True
         user.save(using=self._db)

         return user




# AbstractBaseUser and PermissionsMixin are parent classes
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system""" #docstring
    email=models.EmailField(max_length=255, unique=True) #email should be unique for everu user
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True) #use to activate and deactivate user if needed
    is_staff=models.BooleanField(default=False) #if we need a staff user in system, we can set it to true, and does not have admin access

#required for custom userprofile model, it is used to control users
    objects= UserProfileManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name']

# functions  to interact with custom user model
    def get_full_name(self):
        """Return full name of user"""
        return self.name

# same name as full name for this proj
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

#recommended for all django models for a meaningful output
    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
   """Profile status update"""

   # in setting.py AUTH_USER_MODEL is defined as UserProfile
   user_profile = models.ForeignKey(
   settings.AUTH_USER_MODEL,
    on_delete = models.CASCADE #if user deleted ProfileFeedItem will be removed
   )
   status_text = models.CharField(max_length=255)
   created_on=models.DateTimeField(auto_now_add=True)

   def __str__():
       """Return the model as string"""
       return self.status_text
