from django.contrib import admin
from . models import Category, Product, ShopCart, Slide,Payment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','image')

class ProductAdmin (admin.ModelAdmin):
    list_display = ('id','category','name','price','image','min','max','featured','latest','available')

class SlideAdmin(admin.ModelAdmin):
    list_display = ('id','image','title','comment')

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','basket_no','quantity','paid_order','total')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','amount','basket_no','pay_code','paid_order', 'first_name', 'last_name','phone','address', 'city', 'state')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Slide,SlideAdmin)
admin.site.register(Payment,PaymentAdmin)