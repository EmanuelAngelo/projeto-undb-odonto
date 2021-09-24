from rest_framework.exceptions import ValidationError
from box.utils import BoxEnum
from django.db import models
from django import forms
from datetime import datetime
from user.models import Usuario
from colorfield.fields import ColorField
from django.urls import reverse


# Create your models here.
class TimesTampsModel (models.Model):
    ativo = models.BooleanField(default = True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, auto_now=False, null=True)
    alterado_em = models.DateTimeField('Alterado em', auto_now_add=False, auto_now=True, null=True)
    criado_por = models.CharField('Criado por', max_length=50, null=True, blank=True)
    alterado_por = models.CharField('Alterado por', max_length=50, null=True, blank=True)
    criado_navegador = models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')
    editado_navegador = models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')

    def _criado_por(self):
        return self.criado_em.now.strftime('%d/%m/%Y')
    
    def _alterado_em(self):
        return self.alterado_em.strftime('%d/%m/%Y')
    
    def get_criado_em(self):
        try:
            data = self.criado_em.strftime('%d/%m/%Y %H:%M:%S')
        except:
            data = None
        return data

    class Meta:
        abstract=True


class Caixas (TimesTampsModel): #Box, comparando com admin odonto já criado
    tipo_d_volume = (
        ('Pacote', 'Pacote'),
        ('Caixa', 'Caixa')
    )
    tipo_volume = models.CharField(max_length=10, choices=tipo_d_volume, blank=False, null=False)
    nome_volume = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.nome_volume

    """def get_rud_url(self):
        return reverse('box:caixas_rud', args=(self.id))"""

    class Meta:
        verbose_name_plural = 'Caixa'

class Situacao (TimesTampsModel): #Situação, comparando com admin odonto já criado
    classificacao = models.CharField( max_length=50, verbose_name= 'Nome', blank=True, )
    color = ColorField(default='')
    estatus = models.BooleanField(default = True)
    autorizar = models.BooleanField(default=False, verbose_name='Habilita pedido de autorização')

    def __str__(self):
        return self.classificacao

    """def get_rud_url(self):
        return reverse('box:situacao_rud', args=(self.id))"""

    class Meta:
        verbose_name = 'Situação'

class Deposito (TimesTampsModel): #Deposito, comparando com admin odonto já criado
    usuario = models.ForeignKey(Usuario, related_name='Usuario', on_delete=models.PROTECT, blank=False, null=True, verbose_name='Usuário')
    autorizado = models.BooleanField(default=False, verbose_name='Autorizado')
    #situacao = models.CharField(max_length=50, default=BoxEnum.ESTERILIZAR.name, choices=[(c.name, c.value) for c in BoxEnum])

    #situação para todo o deposito (botao de entrega)
    

    """"    
    def situacao(self):
        situacao = BoxEnum.ESTERILIZAR.name
        if self.situacao == BoxEnum.ESTERILIZAR.name:
            situacao = BoxEnum.ESTERILIZANDO.name
        elif self.situacao == BoxEnum.ESTERILIZANDO.name:
            situacao = BoxEnum.ESTERILIZADO.name
        elif self.situacao == BoxEnum.ESTERILIZADO.name:
            situacao = BoxEnum.ENTREGUE.name
        else:
            return None
        return reverse('box:rud_api_depositosituacao', kwargs={'pk':self.id, 'method':situacao})     
        #testes acima 
    """

    def existe_itens_pendentes(self):
        return self.itens.filter(~models.Q(situacao=BoxEnum.ENTREGUE.name)).exists()

    def esta_aguardando_entrega(self):
        return self.itens.filter(situacao=BoxEnum.ESTERILIZADO.name).exists()
    
    def itens_entregues(self):
        return self.itens.filter(situacao=BoxEnum.ENTREGUE.name).exists()



    def id_padrao(self): #criar regra de numeros a esquerda
        return f'{self.id:07}' #metodo logica de construção de zeros a esquerda

    #id = 10
    #print(f'id={id:06}')
    def qtd_tamanho(self, obj): #logica pegada do projeto de moura
        qt = []
        for a in obj.qtds_deposito.all(): #append insirir na lista
            qt.append(dict(
                id = obj.id,
                caixa = a.caixa.text,
                quantidade = a.quantidade,
                atualizado_por = a.atualizado_por,
                criado_por = a.criado_por,
            ))
        return qt
    
    def qtd_tamanho_total(self, obj):
        qt = 0
        for a in obj.qtds_deposito.all():
            qt +=a.quantidade
        return qt
    
    def qtd_tamanho_(self, obj):
        qttm = ''
        tm = ''
        bx = ''
        qtd = 0
        obs = ''
        usu = ''
        for a in obj.qtds_deposito.all():
            bx += f'{a.caixa.text}'
            qttm += f'{a.quantidade}'
            qtd += a.quantidade
            obs += f'{a.observacoes}'
        return dict(
            id = obj.id,
            caixa = bx.rstrip(),
            tamanho = qttm.rstrip(),
            quantidade = qtd,
            observacoes = obs.rstrip(),
            atualizado_por = obj.atualizado_por,
            criado_em = obj.criado_em
        )

    def autoriza(self, obj):
        auth = []
        for a in obj.autoriza_deposito.all():
            if a.situacao:
                auth.append(dict(
                    id = a.situacao.id,
                    ativo = a.ativo,
                    autorizacao = a.id,
                    autorizado = a.autorizado,
                    update_url = reverse('caixa:autorizacao_rud', args=(a.id,)),
                    value = a.situacao.id,
                    text = a.situacao.text,
                    color = a.situacao.color,
                    data = a.criado_por.strftime('%d/%m/%Y %H:%M:%S'),
                    status = 'Autorizado' if a.autorizado == True else 'Não Autorizado',
                    color_auth = 'green' if a.autorizado == True else 'red'
                ))
        return auth
        
    def __str__(self):
        return f'{self.id} - {self.usuario} - {self.criado_em}'

    def get_rud_url(self):
        return reverse('box:rud_api_deposito', kwargs={'pk':self.id})
    
    class Meta:
        verbose_name_plural = 'Depósito'



class DepositoItem (TimesTampsModel):
    deposito = models.ForeignKey(Deposito, related_name='itens', on_delete=models.CASCADE, verbose_name='Deposito')
    tipo_box = models.ForeignKey(Caixas, on_delete = models.PROTECT, related_name="itens", verbose_name = 'Material',) 
    quantidade = models.IntegerField(verbose_name='Quantidade', blank=True, null=True)
    observacoes = models.TextField(verbose_name='Observações', blank=True, null=True)
    situacao = models.CharField(max_length=50, default=BoxEnum.ESTERILIZAR.name, choices=[(c.name, c.value) for c in BoxEnum])

    def __str__(self):
        return f'{self.id} - {self.deposito}'
    
    def id_padrao(self): #criar regra de numeros a esquerda
        return f'{self.id:07}' #metodo logica de construção de zeros a esquerda
    
    def id_master(self):
        return f'{self.deposito.id:07}'

    def get_depositante_nome(self):
        return f'{self.deposito.usuario.first_name} {self.deposito.usuario.last_name}'
    
    def get_depositante_username(self):
        return f'{self.deposito.usuario.username}'

    #criar um similar para status do confirmar
    def get_next_situacao_url(self):
        situacao = BoxEnum.ESTERILIZAR.name
        if self.situacao == BoxEnum.ESTERILIZAR.name:
            situacao = BoxEnum.ESTERILIZANDO.name
        elif self.situacao == BoxEnum.ESTERILIZANDO.name:
            situacao = BoxEnum.ESTERILIZADO.name
        elif self.situacao == BoxEnum.ESTERILIZADO.name:
            situacao = BoxEnum.ENTREGUE.name
        else:
            return None
        return reverse('box:rud_api_depositoitem', kwargs={'pk':self.id, 'method':situacao})

    # replica para notificar no 'confirm' js
    def get_next_situacao(self):
        situacao = BoxEnum.ESTERILIZAR.value
        if self.situacao == BoxEnum.ESTERILIZAR.name:
            situacao = BoxEnum.ESTERILIZANDO.value
        elif self.situacao == BoxEnum.ESTERILIZANDO.name:
            situacao = BoxEnum.ESTERILIZADO.value
        elif self.situacao == BoxEnum.ESTERILIZADO.name:
            situacao = BoxEnum.ENTREGUE.value
        else:
            return ''
        return situacao
    
    def get_next_situacao_name(self):
        situacao = BoxEnum.ESTERILIZAR.name
        if self.situacao == BoxEnum.ESTERILIZAR.name:
            situacao = BoxEnum.ESTERILIZANDO.name
        elif self.situacao == BoxEnum.ESTERILIZANDO.name:
            situacao = BoxEnum.ESTERILIZADO.name
        elif self.situacao == BoxEnum.ESTERILIZADO.name:
            situacao = BoxEnum.ENTREGUE.name
        else:
            raise ValidationError("Situação não informada")
        return situacao

    #criar botao de capturar todos itens
    def get_next_itensdeposito_url(self):
        situacao = BoxEnum.ESTERILIZAR.name
        if self.situacao == BoxEnum.ESTERILIZAR.name:
            situacao = BoxEnum.ESTERILIZANDO.name
        elif self.situacao == BoxEnum.ESTERILIZANDO.name:
            situacao = BoxEnum.ESTERILIZADO.name
        elif self.situacao == BoxEnum.ESTERILIZADO.name:
            situacao = BoxEnum.ENTREGUE.name
        else:
            return None
        return reverse('box:rud_api_itensdeposito', kwargs={'pk':self.id, 'method':situacao})
    

    def set_esterilizar(self):
        self.situacao = BoxEnum.ESTERILIZAR.name
        return self.save()

    def set_esterilizando(self):
        self.situacao = BoxEnum.ESTERILIZANDO.name
        return self.save()

    def set_esterilizado(self):
        self.situacao = BoxEnum.ESTERILIZADO.name
        return self.save()

    def set_entregue(self):
        self.situacao = BoxEnum.ENTREGUE.name
        return self.save()

    class Meta:
        verbose_name = 'Deposito e Quantidade' 


class LogDepositoItem(models.Model):
    deposito_item = models.ForeignKey(DepositoItem, related_name="logs_item", blank=False, null=True, on_delete=models.CASCADE)
    situacao = models.CharField(max_length=50, default=BoxEnum.ESTERILIZAR.name, choices=[(c.name, c.value) for c in BoxEnum])
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return f'{self.deposito_item.id} - {self.situacao}'
    
    

    def get_criado_em(self):
        try:
            data = self.criado_em.strftime('%d/%m/%Y %H:%M:%S')
        except:
            data = None
        return data


class Autorizacao (TimesTampsModel):
    deposito = models.ForeignKey(Deposito, related_name='autorizacoes', on_delete=models.PROTECT, verbose_name='Deposito')
    situacao = models.ForeignKey(Situacao, related_name='autorizacoes', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Situação') 
    autorizado = models.BooleanField(default=True,verbose_name="Autorizado")

    def __int__(self):
        return self.id
    
    """def get_rud_url(self):
        return reverse('box:autorizacao_rud', args=(self.id))"""
    
    class Meta:
        verbose_name_plural = 'Autorizações'
