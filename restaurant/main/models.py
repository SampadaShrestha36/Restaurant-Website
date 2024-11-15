from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
categoryitems=(
    ("buff","buff"),
    ("chicken","chicken"),
    ("veg","veg")
)

class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phonenumber=PhoneNumberField(null=True,region='NP')
    message=models.TextField()

class Management(models.Model):
    category=models.CharField(choices=categoryitems, max_length=50)
    title=models.CharField( max_length=200)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to='image')

    def __str__(self):
        return self.title
    