from django.db import models

# Create your models here.
class ActiveBookManager(models.Manager):
    def get_queryset(self):
        return super(ActiveBookManager, self).get_queryset().filter(is_active="Y")

class InActiveBookManager(models.Manager):
    def get_queryset(self):
        return super(InActiveBookManager, self).get_queryset().filter(is_inactive="N")


class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    is_active = models.CharField(max_length=1,default="Y")
    is_inactive = models.CharField(max_length=1,default="N")
    active_objects = ActiveBookManager()
    inactive_objects = InActiveBookManager()
    objects = models.Manager()

    
    class Meta:
        db_table = "book"

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)


class ProductVideo(models.Model):
    video = models.ImageField(blank=True)
    
    def __str__(self):
        return self.video

    class Meta:
        db_table = "prodvideo"

