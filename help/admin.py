from app.admin import BaseModelAdmin, admin_site
from .models import Help, HelpCategory


class HelpCategoryAdmin(BaseModelAdmin):
    list_display = [
        helpCategory.name
        for helpCategory in HelpCategory._meta.get_fields()
        if not helpCategory.is_relation
    ]
    search_fields = ["name"]
    list_filter = ["name"]


class HelpAdmin(BaseModelAdmin):
    list_display = [
        help.name for help in Help._meta.get_fields() if not help.is_relation
    ]
    search_fields = ["title"]
    list_filter = ["category__name"]


admin_site.register(Help, HelpAdmin)
admin_site.register(HelpCategory, HelpCategoryAdmin)
