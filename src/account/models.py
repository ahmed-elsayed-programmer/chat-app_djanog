from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin


class MyAccountManager(BaseUserManager):

  def create_user(self , email , username , password= None ):
    if not email :
      raise ValueError("User must have an email address")
    if not username :
      raise ValueError("User must have a username")
    
    user = self.model( 
      email = self.normalize_email(email)  ,
      username = username ,
      )
    user.set_password(password)
    user.save(using= self._db)
    return user 

  def create_superuser(self , email, username ,password):
    user = self.create_user(
      email = self.normalize_email(email),
      username= username ,
      password= password
    )
    user.is_admin = True
    user.is_superuser = True
    user.is_staff = True
    user.save(using = self._db)
    return user   






def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'


def getDefaultImage():
  return "user.png"
# Create your models here.

class Account(AbstractBaseUser ):
  email = models.EmailField( verbose_name= "email" ,  max_length=254 , unique=True)
  username = models.CharField(max_length=250, unique=True  )
  date_joined = models.DateTimeField(verbose_name="last login" ,  auto_now_add=True)
  last_login = models.DateTimeField(verbose_name="last login" , auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  
  profie_image = models.ImageField( upload_to=get_profile_image_filepath, max_length=255 , null= True , blank = True , default = "user.png")
  hide_email = models.BooleanField(default= True)
  objects = MyAccountManager()


  USERNAME_FIELD = 'email' 
  REQUIRED_FIELDS = ['username']

  def __str__(self) :
      return  self.username 

  
  def get_profile_image_filename(self):
    return str(self.profile_image)[str(self.profie_image).index(f"profie_images/{self.pk}/"):]

  def has_perm(self, perm , obj= None ):
      return self.is_admin 
    
  def has_module_perms(self, app_label):
      return True
    

