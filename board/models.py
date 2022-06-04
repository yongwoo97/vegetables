from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(default=1)
    name = models.CharField(primary_key=True, null=False, blank=False, max_length=300)
    unit_price = models.IntegerField(default=0, blank=True, null=False)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

class ProductList(models.Model):
    product_name = models.ForeignKey(Product, related_name='product_list', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='product_loc_list', on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(Unit, related_name='product_unit_list', on_delete=models.DO_NOTHING)

    serial = models.CharField(primary_key=True, max_length=200)
    in_date = models.DateField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    sold_date = models.DateField(null=True, blank=True)
    amount = models.IntegerField(default=0, blank=True, null=False)

    def __str__(self):
        return self.serial
