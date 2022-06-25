from django.contrib import admin
from . import models

admin.site.register(models.ProductList)
admin.site.register(models.Product)
admin.site.register(models.Unit)
admin.site.register(models.Location)

