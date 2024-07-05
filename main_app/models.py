from django.db import models
from authentication.models import Farmer
from django.db.models.signals import post_save
from django.dispatch import receiver

class Operation(models.Model):
    operation_id = models.AutoField(auto_created=True,primary_key=True,unique=True)
    operation_name = models.CharField(max_length=255,help_text="Required, enter operation name here")
    operation_status = models.CharField(choices=(('AVAILABLE','AVAILABLE'),('UNAVAILABLE','UNAVAILABLE')),max_length=155,default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.operation_name}"
    

    class Meta:
        ordering = ["-date_added"]


class Equipment(models.Model):
    eqiupment_id = models.AutoField(auto_created=True,primary_key=True,unique=True)
    eqiupment_name = models.CharField(max_length=255,help_text="Required, enter equipment name here")
    eqiupment_status = models.CharField(choices=(('AVAILABLE','AVAILABLE'),('UNAVAILABLE','UNAVAILABLE')),max_length=155,default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.eqiupment_name}"
    

    class Meta:
        ordering = ["-date_added"]

class Payment(models.Model):

    CHOICES = (('FULL PAID','FULL PAID'),('HALF PAID','HALF PAID'))

    payment_id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    reservation = models.ForeignKey('Reservation',on_delete=models.CASCADE,max_length=255,default="")
    payment_amount = models.CharField(max_length=255,help_text="User has a balance? <a href='#' id='edit_amount'>Click here to edit</a>")
    balance = models.CharField(max_length=255,help_text="Optional if half payment only, enter here if there is a payment balance",null=True)
    payment_type = models.CharField(choices=CHOICES,help_text="Required, select what type of payment",max_length=155,default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.reservation.farmer.first_name} {self.reservation.farmer.last_name}'s payment information" 

@receiver(post_save,sender=Payment)
def payment_save_post_save(sender,instance,created,*args,**kwargs):
    if created and instance.payment_type == 'FULL PAID':
        instance.reservation.reservation_status = 'DONE OPERATION'
        instance.reservation.payment_status = 'FULLY PAID'
        instance.reservation.save()
    
    if created and instance.payment_type == 'HALF PAID':
        instance.reservation.reservation_status = 'DONE OPERATION'
        instance.reservation.payment_status = 'HALF PAID'
        instance.reservation.save()

class Reservation(models.Model):

    class Status(models.TextChoices):
        CANCEL = "CANCEL",'CANCEL'

    class PaymentStatus(models.TextChoices):
        UNPAID = "UNPAID",'UNPAID'
        HALF_PAID = "HALF PAID",'HALF PAID'
        FULL_PAID = "FULLY PAID",'FULLY PAID'

    CHOICES = (
        ('PENDING','PENDING'),
        ('CONFIRMED','CONFIRMED'),
        ('CANCEL','CANCEL')
    )
    
    reservation_id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,help_text="Required, select user here",max_length=255,default="")
    schedule = models.DateField(help_text="Required, add your schedule here.",null=True)
    end_date = models.DateField(help_text="Required, add your end date here.",null=True)
    operation_id = models.ForeignKey(Operation,on_delete=models.CASCADE,help_text="Required, select operation here",max_length=255,null=True,default="")
    reservation_status = models.CharField(choices=(('ONGOING OPERATION','ONGOING OPERATION'),('DONE OPERATION', 'DONE OPERATION')),help_text="Required, select if the operation status",max_length=155,default="",null=True)
    confirmation = models.CharField(choices=CHOICES,max_length=50,default=CHOICES[0][0],null=True)
    equipment = models.ForeignKey(Equipment,on_delete=models.CASCADE,help_text="Select equipment for operation.",default="",null=True,limit_choices_to={'eqiupment_status':'AVAILABLE'})
    payment_status = models.CharField(max_length=150,choices=PaymentStatus.choices,default='UNPAID',null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self) -> str:
        return f"{self.farmer.first_name} {self.farmer.last_name}'s reservation information for {self.equipment.eqiupment_name} equipment"
    
    def save_model(self, request, obj, form, change):
        update_fields = []

        if change: 
            if form.initial['tax_rate'] != form.cleaned_data['tax_rate']:
                update_fields.append('tax_rate')

        obj.save(update_fields=update_fields)

            
