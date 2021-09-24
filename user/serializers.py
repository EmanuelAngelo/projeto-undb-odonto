from rest_framework import serializers
from user.models import Usuario


class UserSerializer(serializers.ModelSerializer):
	"""
	ultimo_login = serializers.SerializerMethodField()
	nome_completo = serializers.SerializerMethodField()
	desde = serializers.SerializerMethodField()
	criado_em = serializers.SerializerMethodField()
	alterado_em = serializers.SerializerMethodField()
	update_url = serializers.SerializerMethodField()

	def get_ultimo_login(self, obj):
		return obj.last_login.strftime('%d/%m/%Y %H:%M:%S') if obj.last_login else obj.last_login
	
	def get_update_url(self, obj):
		return obj.get_rud_url()
	def get_criado_em(self, obj):
		return obj.created_at.strftime('%d/%m/%Y %H:%M:%S') if obj.created_at else obj.created_at
	
	def get_alterado_em(self, obj):
		return obj.updated_at.strftime('%d/%m/%Y %H:%M:%S') if obj.updated_at else obj.updated_at
	def get_nome_completo(self, obj):
		return f'{obj.first_name} {obj.last_name}'

	def get_desde(self, obj):
		return obj.date_joined.strftime('%d/%m/%Y %H:%M:%S') if obj.date_joined else obj.date_joined
	"""

	class Meta:
		model = Usuario
		fields = '__all__'

