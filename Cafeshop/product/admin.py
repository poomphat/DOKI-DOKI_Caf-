from django.contrib import admin
from django.contrib.auth.models import Permission, User
from product.models import Fruit, Drink_info,Customer,Option,Promotion
# Register your models here.

class UserGroupAdmin(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'
    list_display = ['username', 'email', 'first_name', 'last_name', 'group', 'is_staff']
    search_fields = ['username', 'group']
    list_per_page = 10

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']
    list_per_page = 10

class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'fruit_name', 'useable_status']
    list_per_page = 10

class DrinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'd_name', 'cost', 'drink_type', 'useable_status']
    list_per_page = 10

class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'option_name', 'price', 'useable_status']
    list_per_page = 10

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 's_date', 'e_date', 'discount', 'promo_status']
    list_per_page = 10

admin.site.register(Permission)
admin.site.unregister(User)
admin.site.register(User, UserGroupAdmin)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Drink_info, DrinkAdmin)
admin.site.register(Fruit, FruitAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Promotion, PromotionAdmin)