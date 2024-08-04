from app.admin import BaseModelAdmin, admin_site
from .models import Field


class FieldAdmin(BaseModelAdmin):
    list_display = [
        field.name for field in Field._meta.get_fields() if not field.is_relation
    ]
    search_fields = ["name"]
    list_filter = ["status", "field_type"]


admin_site.register(Field, FieldAdmin)
