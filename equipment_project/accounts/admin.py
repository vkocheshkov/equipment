from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_superuser"]
    fieldsets = tuple(
        (
            fieldset[0],
            {
                # Preserve any entries in the dict other than "fields".
                **{key: value for (key, value) in fieldset[1].items() if key != "fields"},
                # Add the "bio" field to the existing fields
                "fields": fieldset[1]["fields"],
            },
        )
        if fieldset[0] == "Personal info"
        else fieldset
        for fieldset in UserAdmin.fieldsets
    )


admin.site.register(CustomUser, CustomUserAdmin)
