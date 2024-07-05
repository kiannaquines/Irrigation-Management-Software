from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'ADMIN'
        FARMER = "FARMER",'FARMER'

    base_role = Role.ADMIN

    gender = models.CharField(choices=(('1','Male'),('2','Female')),max_length=255,help_text="Select your approriate gender",null=True,default="")
    address = models.CharField(max_length=150,help_text="Enter your precise address",null=True)
    mobile = models.CharField(max_length=150,help_text="Enter your mobile number",null=True)
    role = models.CharField(choices=Role.choices,max_length=30,default=base_role,help_text="Required, when you select a farmer, farmer profile will automatically added.")



class FarmerManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs) -> QuerySet:
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.FARMER) 

class FarmerLandInformation(models.Model):
    # owner information
    user = models.OneToOneField('Farmer',on_delete=models.CASCADE)

    # land information
    lot_number = models.CharField(max_length=255,help_text="Enter land lot number",null=True)
    hectares = models.FloatField(help_text="Enter land size in hectares",null=True)
    square_meter = models.PositiveBigIntegerField(help_text="Enter land size square meter",null=True)
    region = models.CharField(max_length=150,help_text="Enter land location region",null=True)
    province = models.CharField(max_length=150,help_text="Enter land provice",null=True)
    municipality = models.CharField(max_length=150,help_text="Enter land location municipality",null=True)
    barangay = models.CharField(max_length=150,help_text="Enter land location barangay",null=True)
    long = models.FloatField(help_text="Enter land longitude", null=True)
    lat = models.FloatField(help_text="Enter land latitude", null=True)


    # land image
    image = models.ImageField(upload_to="land/",null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} Land Information'


class Farmer(User):
    base_role = User.Role.FARMER
    farmer = FarmerManager()

    def save(self,*args,**kwargs):
        if not self.pk:
            self.is_active = False
            self.role = self.base_role
            return super().save(*args,**kwargs)

    class Meta:
        proxy = True


@receiver(post_save,sender=Farmer)
def create_farmer_profile(sender,instance,created,**kwargs):
    if created and instance.role == "FARMER":
        FarmerLandInformation.objects.create(user=instance)

@receiver(post_save,sender=User)
def create_farmer_profile_from_admin(sender,instance,created,*args,**kwargs):
    if created and instance.role == "FARMER":
        print("Send to email", instance.username)
        FarmerLandInformation.objects.create(user=instance)




