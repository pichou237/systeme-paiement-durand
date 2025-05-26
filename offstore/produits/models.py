from django.db import models

class Produit(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="produit_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
# Create your models here.
