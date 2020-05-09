from django.db import models

# Create your models here.
class Image(models.Model):
    pic1 = models.ImageField(blank=False, upload_to="images/%Y/%m/%d")
    pic2 = models.ImageField(blank=False, upload_to="images/%Y/%m/%d")
    pic3 = models.ImageField(blank=False, upload_to="images/%Y/%m/%d")

    # def __str__(self):
    #     return self.pic