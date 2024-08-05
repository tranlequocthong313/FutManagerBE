from app.admin import BaseModelAdmin, admin_site
from .models import Introduction


class IntroductionAdmin(BaseModelAdmin):
    list_display = [
        introduction.name
        for introduction in Introduction._meta.get_fields()
        if not introduction.is_relation
    ]
    search_fields = ["version"]
    list_filter = ["version"]


admin_site.register(Introduction, IntroductionAdmin)
