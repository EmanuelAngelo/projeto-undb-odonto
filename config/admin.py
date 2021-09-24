from django.contrib import admin
from .models import Config
import datetime
# Register your models here.

class ListandoConfig(admin.ModelAdmin):
    list_display = ('descricao',)
    filter_horizontal = ('conf_situacao','conf_autorizacao')

    def save_model(self, request, obj, form, change):
        if change:
            obj.alterado_em = datetime.datetime.now()
            obj.alterado_por = request.user.username
        else:
            obj.criado_em = datetime.datetime.now()
            obj.criado_por = request.user.username
        super(ListandoConfig, self).save_model(request, obj, form, change)

admin.site.register(Config, ListandoConfig)