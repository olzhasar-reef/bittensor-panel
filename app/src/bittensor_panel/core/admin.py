from django.contrib import admin, messages
from django.contrib.admin import register
from django.http.response import (
    HttpResponseRedirect,
)
from django.urls import path, reverse

from .exceptions import BittensorAPIError, HyperParameterUpdateFailed
from .models import HyperParameter
from .services import (
    refresh_hyperparams,
    update_hyperparam,
)


@register(HyperParameter)
class HyperParameterAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "created_at", "updated_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        try:
            update_hyperparam(obj)
        except (BittensorAPIError, HyperParameterUpdateFailed) as e:
            messages.error(request, str(e))

    def get_urls(self):
        urls = [
            path(
                "refresh-hyperparams/",
                self.admin_site.admin_view(self.refresh_hyperparams_view),
                name="refresh_hyperparams",
            ),
        ]
        urls += super().get_urls()
        return urls

    def refresh_hyperparams_view(self, request):
        if request.method == "POST":
            try:
                refresh_hyperparams()
            except BittensorAPIError as e:
                messages.error(request, str(e))

        return HttpResponseRedirect(reverse("admin:core_hyperparameter_changelist"))


admin.site.site_header = "Bittensor Administration Panel"
admin.site.site_title = "Bittensor Administration Panel"
admin.site.index_title = "Welcome to Bittensor Administration Panel"
