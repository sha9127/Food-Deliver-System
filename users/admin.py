from django.contrib import admin
from .models import BaseModel, Role, User

# Register your models here.
# admin.site.register(BaseModel)
admin.site.register(Role)
admin.site.register(User)


# UserAdmin.fieldsets += ('Custom Field Set',
#                         {'fields': ('image', 'address', 'Type',)}),
