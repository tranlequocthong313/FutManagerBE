from app.admin import BaseModelAdmin, admin_site
from .models import Review


class ReviewAdmin(BaseModelAdmin):
    list_display = [
        review.name for review in Review._meta.get_fields() if not review.is_relation
    ]
    search_fields = ["field__name", "user__full_name"]
    list_filter = ["rating", "field__name", "field__field_type"]


admin_site.register(Review, ReviewAdmin)
