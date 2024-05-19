from django.contrib import admin
from .models import Profile, Product, CartAdd, Category, Order, OrderDetails, ItemRating, Subcategory, Product_Gallary
from django.contrib.admin.options import ModelAdmin

# Register your models here.
admin.site.site_header = 'Bloomflow Admin Dashboard'


class UserProfile(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Profile, UserProfile)


class P_Gallary(ModelAdmin):
    list_display = ['Productid']


admin.site.register(Product_Gallary, P_Gallary)


class UserOrder(ModelAdmin):
    list_display = ['odate', 'p_mode', 'made_by', 'order_id']
    search_fields = ['user']


admin.site.register(Order, UserOrder)


class UserProduct(ModelAdmin):
    list_display = ['Pname']
    search_fields = ['Plight']


admin.site.register(Product, UserProduct)


class UserCartAdd(ModelAdmin):
    search_fields = ['product']
    list_display = ['id']


admin.site.register(CartAdd, UserCartAdd)


class UserOrderDetails(ModelAdmin):
    list_display = ['user']
    search_fields = ['product']


admin.site.register(OrderDetails, UserCartAdd)


class UserCategory(ModelAdmin):
    search_fields = ['C_disc']


admin.site.register(Category, UserCategory)


class UserSubcategory(ModelAdmin):
    search_fields = ['Scname']
    list_filter = ['category']


admin.site.register(Subcategory, UserSubcategory)


class UserItemRating(ModelAdmin):
    list_display = ['title']
    search_fields = ['product']


admin.site.register(ItemRating, UserCategory)
