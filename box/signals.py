from box.models import LogDepositoItem
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DepositoItem, LogDepositoItem, Situacao
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string 
from django.utils.safestring import mark_safe 
from django.conf import settings

class Email():
    #notifca email quando esta esterelizado
    def notificar(self, assunto, to=[], bcc=[], cc=[], reply_to=[], objeto=None,template='box/email_deposito_item.html',nomeDestinatario=''):
        if settings.NOTIFICAR:
            body = render_to_string(template, {'objeto':objeto, 'assunto':assunto, 'nomeDestinatario':nomeDestinatario})
            msg = EmailMessage(assunto, mark_safe(body), to=to, bcc=bcc, cc=cc, reply_to=reply_to)
            msg.content_subtype = 'html'
            msg.send()
    #notificao email no ato da entrega do item
    def notifcarEntrega(self, assunto, to=[], bcc=[], cc=[], reply_to=[], objeto=None,template='box/email_deposito_retirada.html',nomeDestinatario=''):
        if settings.NOTIFICAR:
            body = render_to_string(template, {'objeto':objeto, 'assunto':assunto, 'nomeDestinatario':nomeDestinatario})
            msg = EmailMessage(assunto, mark_safe(body), to=to, bcc=bcc, cc=cc, reply_to=reply_to)
            msg.content_subtype = 'html'
            msg.send()
    
    #notificao email no ato da entrega do item
    def notificarEntregaDeposito(self, assunto, to=[], bcc=[], cc=[], reply_to=[], objeto=None,template='box/email_deposito.html',nomeDestinatario=''):
        if settings.NOTIFICAR:
            body = render_to_string(template, {'objeto':objeto, 'assunto':assunto, 'nomeDestinatario':nomeDestinatario})
            msg = EmailMessage(assunto, mark_safe(body), to=to, bcc=bcc, cc=cc, reply_to=reply_to)
            msg.content_subtype = 'html'
            msg.send()

@receiver(post_save, sender=DepositoItem)
def log_deposito_item(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        #print(instance.__dict__)
        pass