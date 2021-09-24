from pprint import pprint
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
DEFAULT_FORMAT_DATETIME = '%d/%m/%Y %H:%M:%S'

class Usuario(AbstractUser):
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, auto_now=False, null=True)
    alterado_em = models.DateTimeField('Alterado em', auto_now_add=False, auto_now=False, null=True)
    criado_por = models.CharField('Criado por', max_length=50, null=True, blank=True)
    alterado_por = models.CharField('Alterado por', max_length=50, null=True, blank=True)
    token = models.CharField(max_length=250, default=make_password('123456'),blank=True, null=True)
    
    def clean(self):
        if not self.email or self.email == '':
            raise ValidationError('E-mail não informado!')
    
    def _criado_em(self):
        return self.criado_em.strftime(DEFAULT_FORMAT_DATETIME)
    
    def _alterado_em(self):
        return self.alterado_em.strftime(DEFAULT_FORMAT_DATETIME)
    
    def get_cl_url(self):
        return reverse('api:users_cl', args=(self.id,))

    def get_rud_url(self):
        return reverse('api:users_rud', args=(self.id,))

    def get_rud_image_url(self):
        return reverse('api:users_image_rud', args=(self.id,))
    
    def _grupos(self):
        p = ','
        grupos = []
        for gr in self.groups.all():
            grupos.append(gr)
        p.join([str(grupos)])
        return grupos

    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    