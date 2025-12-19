from django.db import models

# Create your models here.

class Donation(models.Model):
    session_id = models.CharField(unique = True, max_length=50)
    email = models.EmailField(null = True, max_length=254 , blank = True)
    amount = models.IntegerField()
    confirmed = models.BooleanField(default= False)
    created_at = models.DateTimeField( auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = ("Donation")
        verbose_name_plural = ("Donations")

    def __str__(self):
        return str(self.pk)
