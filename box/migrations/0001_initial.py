# Generated by Django 2.1.15 on 2021-07-16 09:25

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autorizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em')),
                ('criado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Criado por')),
                ('alterado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alterado por')),
                ('criado_navegador', models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')),
                ('editado_navegador', models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')),
                ('autorizado', models.BooleanField(default=True, verbose_name='Autorizado')),
            ],
            options={
                'verbose_name_plural': 'Autorizações',
            },
        ),
        migrations.CreateModel(
            name='Caixas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em')),
                ('criado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Criado por')),
                ('alterado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alterado por')),
                ('criado_navegador', models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')),
                ('editado_navegador', models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')),
                ('tipo_volume', models.CharField(choices=[('Pacote', 'Pacote'), ('Caixa', 'Caixa')], max_length=10)),
                ('nome_volume', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Caixa',
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em')),
                ('criado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Criado por')),
                ('alterado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alterado por')),
                ('criado_navegador', models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')),
                ('editado_navegador', models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')),
                ('autorizado', models.BooleanField(default=False, verbose_name='Autorizado')),
            ],
            options={
                'verbose_name_plural': 'Depósito',
            },
        ),
        migrations.CreateModel(
            name='DepositoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em')),
                ('criado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Criado por')),
                ('alterado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alterado por')),
                ('criado_navegador', models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')),
                ('editado_navegador', models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')),
                ('quantidade', models.IntegerField(blank=True, null=True, verbose_name='Quantidade')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('situacao', models.CharField(choices=[('ESTERILIZAR', 'A Esterilizar'), ('ESTERILIZANDO', 'Esterilizando'), ('ESTERILIZADO', 'Esterilizado'), ('ENTREGUE', 'Entregue')], default='ESTERILIZAR', max_length=50)),
                ('deposito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='box.Deposito', verbose_name='Deposito')),
                ('tipo_box', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itens', to='box.Caixas', verbose_name='Material')),
            ],
            options={
                'verbose_name': 'Deposito e Quantidade',
            },
        ),
        migrations.CreateModel(
            name='LogDepositoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situacao', models.CharField(choices=[('ESTERILIZAR', 'A Esterilizar'), ('ESTERILIZANDO', 'Esterilizando'), ('ESTERILIZADO', 'Esterilizado'), ('ENTREGUE', 'Entregue')], default='ESTERILIZAR', max_length=50)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('deposito_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs_item', to='box.DepositoItem')),
            ],
        ),
        migrations.CreateModel(
            name='Situacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em')),
                ('criado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Criado por')),
                ('alterado_por', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alterado por')),
                ('criado_navegador', models.TextField(blank=True, null=True, verbose_name='Criado no Navegador')),
                ('editado_navegador', models.TextField(blank=True, null=True, verbose_name='Editado no Navegador')),
                ('classificacao', models.CharField(blank=True, max_length=50, verbose_name='Nome')),
                ('color', colorfield.fields.ColorField(default='', max_length=18)),
                ('estatus', models.BooleanField(default=True)),
                ('autorizar', models.BooleanField(default=False, verbose_name='Habilita pedido de autorização')),
            ],
            options={
                'verbose_name': 'Situação',
            },
        ),
    ]