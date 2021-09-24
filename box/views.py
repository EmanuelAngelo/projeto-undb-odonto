from box.signals import Email
import re
from django.db import models
from box.utils import BoxEnum
from django.shortcuts import render
from django.views.generic import TemplateView
from gdbundbrm.custom_views import RMCustomListCreateAPIView, RMCustomRetrieveUpdateDestroyAPIView
from rest_framework import generics, serializers, status
from rest_framework.exceptions import ValidationError
from box.models import Caixas, Situacao, Deposito, DepositoItem, LogDepositoItem
from user.models import Usuario
from box.serializers import CaixasSerializer, SituacaoSerializer, DepositoSerializer, DepositoItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password




class IndexView(TemplateView):
    template_name="box/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caixas'] = Caixas.objects.all()
        return context


class TesteEmailView(TemplateView): #ver como esta ficando template do email
    template_name="box/email_deposito.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomeDestinatario'] = self.request.user.first_name
        context['assunto'] = 'Assunto Teste'
        serial = DepositoSerializer(Deposito.objects.get(id=1314)).data
        context['objeto'] = serial
        context['teste'] = Deposito.objects.get(id=1314)
        return context


"""class UserAPIView(generics.ListCreateAPIView):
    model = Usuario
    queryset = model.objects.all()

    def get_user(self, request, *args, **kwargs):  #usar para mudar senha do usuario
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        u = User.objects.filter(username=username).first()
        u.set_password(password)
        u.save()
        check_password(password, u.password)
            
        return super().list(request, args, kwargs)"""


from django.db import transaction

class DepositoItemAPIView(RMCustomListCreateAPIView):
    model = DepositoItem
    serializer_class = DepositoItemSerializer
    queryset = model.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save(criado_por=self.request.user.username)
        obj.save()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RUDDepositoItemAPIView(RMCustomRetrieveUpdateDestroyAPIView):
    model = DepositoItem
    serializer_class = DepositoItemSerializer
    queryset = model.objects.all()

    def perform_update(self, serializer):
        obj = serializer.save(alterado_por=self.request.user.username)
        obj.save()
        LogDepositoItem.objects.create(deposito_item=obj, situacao=obj.situacao)

    def patch(self, request, *args, **kwargs):
        print(request.data)
        raise serializers.ValidationError('Teste')

        method = kwargs.get('method', '').lower()
        deposito_item = self.get_object()
        if method and method in [m.name.lower() for m in BoxEnum]:
            pass
        else:
            raise serializers.ValidationError('Método desconhecido')
        #with transaction.atomic():
        if method == BoxEnum.ESTERILIZANDO.name.lower():
            deposito_item.set_esterilizando()
        elif method == BoxEnum.ESTERILIZADO.name.lower():
            deposito_item.set_esterilizado()
            email = Email()
            #msg = f'Item #{deposito_item.id}-{deposito_item.tipo_box.nome_volume} atualizado para status {deposito_item.situacao} '
            email.notificar(assunto='Aguardando retirada de item', to=[deposito_item.deposito.usuario.email],objeto=deposito_item)
        elif method == BoxEnum.ENTREGUE.name.lower():
            deposito_item.set_entregue()
            email = Email()
            email.notifcarEntrega(assunto='Material Entregue', to=[deposito_item.deposito.usuario.email],objeto=deposito_item)
        else:
            deposito_item.set_esterilizar()

        return super().partial_update(request, *args, **kwargs)

# view para atualizar todos depositos item
class RUDDepositoAPIView(RMCustomRetrieveUpdateDestroyAPIView):
    model = Deposito
    serializer_class = DepositoSerializer
    queryset = model.objects.all()

    def perform_update(self, serializer):
        deposito = serializer.save(alterado_por=self.request.user.username)
        deposito.save()
        email = Email()
        with transaction.atomic():
            for deposito_item in deposito.itens.all():
                if deposito_item.situacao != BoxEnum.ENTREGUE.name:
                    deposito_item.situacao = deposito_item.get_next_situacao_name()
                    deposito_item.save()
                    LogDepositoItem.objects.create(deposito_item=deposito_item, situacao=deposito_item.situacao) #log de deposito
       
            email.notificarEntregaDeposito(assunto=f'Nova movimentação do depósito {deposito.id_padrao()}', to=[deposito.usuario.email],objeto=deposito)



class BoxAPIView(generics.ListCreateAPIView):
    model = Caixas
    serializer_class = CaixasSerializer
    queryset = model.objects.all().order_by('nome_volume')
    
    def get(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class SituacaoAPIView(generics.ListCreateAPIView):
    model = Situacao
    serializer_class = SituacaoSerializer
    queryset = model.objects.all()

    def get(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

class DepositoAPIView(RMCustomListCreateAPIView):
    model = Deposito
    serializer_class = DepositoSerializer
    queryset = model.objects.exclude(usuario=None).order_by('-id')

    def perform_create(self, serializer):
        obj = serializer.save(criado_por=self.request.user.username, alterado_por=self.request.user.username)

        #print(obj.usuario, obj.criado_por, obj.alterado_por, self.request.data)
        usuario = self.request.data.get('usuario')
        itens = self.request.data.get('depositos')

        if not itens or not usuario:
            raise ValidationError('Usuário ou Depósitos não informados')
        
        with transaction.atomic():
            try:
                user = Usuario.objects.get(id=usuario)
            except:
                raise ValidationError('Usuário não encontrado')

            obj.usuario = user
            obj.save()

            bulk = []
            for item in itens:
                tipo = Caixas.objects.get(id=item.get('tipo_box'))
                qtde = item.get('quantidade')
                obs = item.get('observacoes')
                bulk.append(DepositoItem(
                    deposito=obj, 
                    tipo_box=tipo, 
                    quantidade=qtde, 
                    observacoes=obs, 
                    criado_por=self.request.user.username
                    ))
            
            DepositoItem.objects.bulk_create(bulk)
        email = Email()
        d = Deposito.objects.filter(id=obj.id).first()
        if d:
            #notificar deposito realizado email
            email.notificar(assunto='Deposito Realizado', to=[d.usuario.email],objeto=d, template='box/email_deposito.html', nomeDestinatario=self.request.user.first_name)
            #return super().perform_create(serializer)


    def get(self, request, *args, **kwargs):
        
        filtro = request.query_params.get('filtro')
        if filtro == 'all':
            pass
        elif filtro == 'entregue' :
            itens = DepositoItem.objects.filter(models.Q(situacao__in=[BoxEnum.ENTREGUE.name])).values('deposito').distinct()
            self.queryset = self.queryset.filter(id__in=itens).order_by('-id')
        else:
            itens = DepositoItem.objects.filter(~models.Q(situacao__in=[BoxEnum.ENTREGUE.name])).values('deposito').distinct()
            self.queryset = self.queryset.filter(id__in=itens).order_by('-id')
        
        #filtrar por usuario logado se não for membro
        if not request.user.is_staff:
            self.queryset = self.queryset.filter(usuario=request.user)
        return super().get(request, *args, **kwargs)



    
