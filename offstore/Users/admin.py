from django.contrib import admin
from .models import User, OneTimePasscode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(OneTimePasscode)
class OneTimePasscodeAdmin(admin.ModelAdmin):
    pass
