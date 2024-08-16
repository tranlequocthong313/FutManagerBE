from app.admin import BaseModelAdmin, admin_site
from user.models import User


class UserAdmin(BaseModelAdmin):
    list_display = [
        user.name for user in User._meta.get_fields() if not user.is_relation
    ]


admin_site.register(User, UserAdmin)
