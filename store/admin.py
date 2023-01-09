from django.contrib import admin
from .models import *


class ImagesTublerinline(admin.TabularInline):
    model = Images

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]
    list_display = ['firstname','lastname','phone','email','paid']
    search_fields = ['firstname','phone','email','payment_id']






admin.site.register(Images)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)
admin.site.register(Categories)
admin.site.register(Brands)
admin.site.register(Contact_us)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

