from django.db.models import fields
from django.db.models.fields.related import ManyToManyField
from base import models
from pprint import pprint
from datetime import datetime
from django.urls import reverse
from rest_framework import serializers
from user.serializers import UserSerializer
from box.models import Caixas, LogDepositoItem, Situacao, Deposito, Autorizacao, DepositoItem


class CaixasSerializer(serializers.ModelSerializer):
    """
    ref = serializers.SerializerMethodField()
    box = serializers.SerializerMethodField()
    quantidade = serializers.SerializerMethodField() 
    observacoes = serializers.SerializerMethodField()
    disabled = serializers.SerializerMethodField()
    check_disabled = serializers.SerializerMethodField()

    def get_ref(self, obj):
        return obj.id

    def get_box(self, obj):
        return ''

    def get_quantidade(self, obj):
        return ''

    def get_observacoes(self, obj):
        return ''

    def get_disabled(self, obj):
        return True

    def get_check_disabled(self, obj):
        return False
    """
    class Meta:
        model = Caixas
        fields = '__all__'

class LogDepositoItemSerializer(serializers.ModelSerializer):
    get_criado_em = serializers.SerializerMethodField()

    def get_get_criado_em(self, obj):
        return obj.get_criado_em()

    class Meta:
        model = LogDepositoItem
        fields ='__all__'

class DepositoItemSerializer(serializers.ModelSerializer):
    logs_item = LogDepositoItemSerializer(many=True, read_only=True)
    tipo_box = CaixasSerializer(many=False, read_only=True)
    get_depositante_nome = serializers.SerializerMethodField()
    get_depositante_username = serializers.SerializerMethodField()
    get_criado_em = serializers.SerializerMethodField()
    get_next_situacao_url = serializers.SerializerMethodField()
    get_next_situacao =  serializers.SerializerMethodField() #notif aba cofirm js
    id_padrao = serializers.SerializerMethodField() # model metodo de zero a esquerda
    id_master = serializers.SerializerMethodField() # model metodo de zero a esquerda


    def get_get_next_situacao(self, obj): #notif aba confirm js
        return obj.get_next_situacao()

    def get_get_next_situacao_url(self, obj):
        return obj.get_next_situacao_url()
    
    def get_get_depositante_nome(self, obj):
        return obj.get_depositante_nome()
    
    def get_get_depositante_username(self, obj):
        return obj.get_depositante_username()
    
    def get_get_criado_em(self, obj):
        return obj.get_criado_em()
    
    def get_id_padrao(self, obj): #retirado do metodo de zero esquerda model
        return obj.id_padrao()
    
    def get_id_master(self, obj): #retirado do metodo de zero esquerda model
        return obj.id_master()
    
    class Meta:
        model = DepositoItem
        fields = '__all__' 


class SituacaoSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    update_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Situacao
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_update_url(self, obj):
        return obj.get_rud_url()

class DepositoSerializer(serializers.ModelSerializer):
    """
    """
    usuario = UserSerializer(many=False, read_only=True)
    #autoriza = serializers.SerializerMethodField()
    #qtd_tamanho = serializers.SerializerMethodField()
    #qtd_tamanho_total = serializers.SerializerMethodField()
    #deposito_situacao = serializers.SerializerMethodField()
    get_rud_url = serializers.SerializerMethodField()
    criado_em = serializers.SerializerMethodField()
    alterado_em = serializers.SerializerMethodField()
    id_padrao = serializers.SerializerMethodField() # model metodo de zero a esquerda
    existe_itens_pendentes = serializers.SerializerMethodField() # model metodo de zero a esquerda
    esta_aguardando_entrega = serializers.SerializerMethodField() # model metodo de zero a esquerda
    itens_entregues = serializers.SerializerMethodField() # model metodo de zero a esquerda
    itens = DepositoItemSerializer(many=True, read_only=True)
    

    class Meta:
        model = Deposito
        fields = '__all__'

    #def get_deposito_situacao(self):
           #return self.deposito_situacao()
        
    def get_id_padrao(self, obj): #retirado do metodo de zero esquerda model
        return obj.id_padrao()

        
    def get_alterado_em(self, obj):
        return obj.alterado_em
    
    def get_existe_itens_pendentes(self, obj):
        return obj.existe_itens_pendentes()
    
    def get_esta_aguardando_entrega(self, obj):
        return obj.esta_aguardando_entrega()
    
    def get_itens_entregues(self, obj):
        return obj.itens_entregues()

    def get_criado_em(self, obj):
        return obj.get_criado_em()

    def get_get_rud_url(self, obj):
        return obj.get_rud_url()
