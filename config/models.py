from django.db import models
from django.contrib.auth.models import Group
from box.models import Situacao

# Create your models here.
class Config (models.Model):
    descricao = models.CharField(verbose_name='Descrição', max_length=50, default='Padrão', null=True)
    ativo = models.BooleanField(verbose_name='Configuração Ativo', default=True)
    conf_situacao = models.ManyToManyField(Situacao, blank=True, related_name='conf_situcao', verbose_name='Oculta a situação para o colaborador')
    conf_autorizacao = models.ManyToManyField(Situacao, blank=True, related_name='conf_autorizacao', verbose_name='Exigir autorização para as situações')
    list_restrito = models.OneToOneField(Group,related_name='grupo_listar_depositoss_restrito', blank=True,null=True,on_delete=models.PROTECT,verbose_name='Lista restrita por usuário de depósitos')
    list_completo = models.OneToOneField(Group,related_name='grupo_listar_depositoss_completo', blank=True,null=True,on_delete=models.PROTECT,verbose_name='Lista geral dos depósitos')
    
    def __str__(self):
        return self.descricao
    
    def clean(self):
        config = Config.objects.filter(~Q(id=self.id)).count()
        if config >0:
            raise ValidationError('Já existe uma configuração registrada em sistema!')
    
    class Meta:
        verbose_name = 'Configuração'
        