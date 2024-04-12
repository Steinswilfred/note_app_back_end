from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your models here.


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)


class Items_Category(models.Model):
        Item_name = models.CharField(max_length=255)

        def __str__(self):
                return self.Item_name
class User_information(models.Model):
        Name = models.CharField(max_length=255)
        Items = models.ForeignKey(Items_Category,related_name='items_names',default=1,on_delete=models.CASCADE)
        Weight = models.DecimalField(max_digits=10,decimal_places=2)
        gl_no = models.IntegerField(unique=True)
        Bgl_no = models.CharField(max_length=255,unique=True)
        Amount = models.PositiveIntegerField()
        Date = models.DateTimeField(auto_now_add=True)
        isDeleted = models.BooleanField(default=False)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        def __str__(self):
            return self.Name