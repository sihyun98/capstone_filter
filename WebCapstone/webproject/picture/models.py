from django.db import models

# Create your models here.
class Image(models.Model):
    pic = models.ImageField(blank=False, upload_to="images/%Y/%m/%d")
    #image = models.ImageField(upload_to="")
    # def __str__(self):
    #     return self.pic


# from django.urls import reverse
# from django.contrib.auth.models import User

# # Create your models here.
# class Store(models.Model):
#     objects=models.Manager()
#     name=models.CharField(max_length=20)
#     num=models.CharField(max_length=20)
#     content = models.TextField()
#     store_pic = models.ImageField(blank=False, upload_to="images/%Y/%m/%d")
#     owner=models.ForeignKey(User,editable=False,on_delete=models.CASCADE,default='1')

#     def __str__(self):
#         return self.name
#     def get_absolute_url(self):
#         return reverse('store:detail',args=[str(self.pk)])