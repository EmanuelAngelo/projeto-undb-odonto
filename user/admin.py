from django.contrib import admin
from user.forms import UsuarioChangeForm
from user.models import Usuario
from django.contrib.auth.admin import UserAdmin
from pprint import pprint

@admin.register(Usuario)
class UserAdmin(UserAdmin):
    # Para incluir o addForm, herdar do UserAdmin
    #add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    list_display = ['username', 'email', 'first_name','last_name','is_active','is_staff', 'is_superuser', 'last_login',]
    list_display_links = ['username', 'email', 'first_name','last_name', 'is_active', 'last_login']
    filter_horizontal = ('user_permissions',)
    readonly_fields = ('date_joined', 'last_login', 'token' )
    list_per_page = 50
    show_full_result_count = True
    autocomplete_fields = ['groups']

    save_as = False  # opção de criar novo usuário a partir de outro já existente
    search_fields = ('username', 'email',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','username','email','password1','password2','is_staff','is_superuser','groups'),
        }),
    )
    """
    """

    fieldsets = (
        ('Usuário', {
            'fields': (('username','email'),'password' )
        }),
        ('Identificação', {
            'classes': ('',),
            'fields': (('first_name','last_name'),),
        }),
        ('Liberação de Acesso', {
            'classes': ('',),
            'fields': (('is_active', 'is_staff'), 'is_superuser', ),
        }),
        ('Permissões', {
            'classes': ('',),
            'fields': ('groups', 'user_permissions'),
        }),
        ('Detalhes', {
            'classes': ('',),
            'fields': ('date_joined',  'last_login', 'token' ),
        }),
    )

    date_hierarchy = 'last_login'
    ordering = ['-id']
    actions = ['ativarUsuario',]

    def save_model(self, request, obj, form, change):
        import datetime
        #print(datetime.datetime.now())
        if change:
            obj.alterado_por = request.user.username
            obj.alterado_em = datetime.datetime.now()
        else:
            obj.criado_por = request.user.username
            obj.criado_em = datetime.datetime.now()

        super(UserAdmin, self).save_model(request, obj, form, change)

    def ativarUsuario(modeladmin, request, queryset):
        for obj in queryset:
            if not obj.is_staff:
                obj.is_active = not obj.is_active
                obj.save()
            else:
                if not obj.is_active:
                    obj.is_active = not obj.is_active
                    obj.save()

    ativarUsuario.short_description = "Ativar/Desativar usuário"
    ativarUsuario.allowed_permissions = ('change',)

    '''''@receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        config = Config.objects.first()
        email = instance.email.split('@') 
        if config.listardepositosrestrito and email[1] == 'aluno.undb.edu.br':
            grupo = Group.objects.get(name=config.listardepositosrestrito)
            grupo.user_set.add(instance)'''''


'''@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    search_fields = ('object_repr',)
    list_filter = ('action_time', 'content_type',)
    list_display = ('action_time', 'user', 'content_type', 'tipo', 'object_repr')
    fields = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message', )
    readonly_fields = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'tipo', 'change_message', )

    def tipo(self, obj):
        if obj.is_addition():
            return u"Adicionado"
        elif obj.is_change():
            return u"Modificado"
        elif obj.is_deletion():
            return u"Deletado"


@admin.register(HistoricoAcesso)
class AcessoAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','ip','acesso_em','so','so_detalhes','dispositivo')
'''
