from django.contrib import admin
from .models import Product,Contact,Customer,Category,Cart,Order,Wishlist,SearchHistory,VisitHistory
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

@admin.register(Category)
class CategoryMdelAdmin(admin.ModelAdmin):
    list_display=['id','title']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','city','mobile','pincode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['id','user','status']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','timestamp']

@admin.register(VisitHistory)
class VisitHistoryModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','timestamp']

@admin.register(SearchHistory)
class SearchHistoryModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','timestamp']





