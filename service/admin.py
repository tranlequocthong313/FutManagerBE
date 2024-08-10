from app.admin import BaseModelAdmin, admin_site
from .models import Introduction, CustomerSupport


class IntroductionAdmin(BaseModelAdmin):
    list_display = [
        introduction.name
        for introduction in Introduction._meta.get_fields()
        if not introduction.is_relation
    ]
    search_fields = ["version"]
    list_filter = ["version"]


class CustomerSupportAdmin(BaseModelAdmin):
    list_display = [
        customersupport.name
        for customersupport in CustomerSupport._meta.get_fields()
        if not customersupport.is_relation
    ]
    search_fields = ["service_name"]


admin_site.register(CustomerSupport, CustomerSupportAdmin)
admin_site.register(Introduction, IntroductionAdmin)
