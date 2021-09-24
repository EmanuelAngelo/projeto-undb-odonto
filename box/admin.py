from django.contrib import admin
from .models import Caixas, LogDepositoItem, Situacao, Deposito, DepositoItem, Autorizacao

# Register your models here.
@admin.register(Caixas)
class ListandoCaixas(admin.ModelAdmin):
    list_display = ('id','tipo_volume', 'nome_volume')

@admin.register(Situacao)
class ListandoSituacao(admin.ModelAdmin):
    list_display = ('classificacao', 'color', 'estatus')

@admin.register(Deposito)
class ListandoDeposito(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'autorizado')

@admin.register(DepositoItem)
class ListandoDepositoItem(admin.ModelAdmin):
    list_display = ('id', 'tipo_box', 'quantidade', 'deposito', 'criado_em')
    readonly_fields = ('criado_por','alterado_por','criado_em','alterado_em')

@admin.register(Autorizacao)
class ListandoAutorizacao(admin.ModelAdmin):
    list_display = ('id', 'deposito', 'situacao')

@admin.register(LogDepositoItem)
class LogDepositoItem(admin.ModelAdmin):
    list_display = ('deposito_item','situacao','criado_em')