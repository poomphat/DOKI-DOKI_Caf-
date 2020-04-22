from django.contrib import admin
from django.contrib.auth.models import Permission, User

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

admin.site.register(Permission)
admin.site.unregister(User)
admin.site.register(User, UserGroupAdmin)