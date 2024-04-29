from django.contrib import admin
from product.models import Product, Image, Inventory, ProductInventory, CustomerReview

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Inventory)
admin.site.register(ProductInventory)
admin.site.register(CustomerReview)
