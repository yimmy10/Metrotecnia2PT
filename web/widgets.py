from django_select2 import forms as s2forms


class ClienteWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "razon_social__icontains",
    ]