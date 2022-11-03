# Generated by Django 4.0.4 on 2022-08-14 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.CharField(default='', max_length=400)),
                ('arteria', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('porta', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('alojamento', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('localidade', models.CharField(blank=True, default='', max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagina', models.CharField(default='', max_length=500)),
                ('tag', models.CharField(default='', max_length=500)),
                ('conteudo', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacao', models.CharField(default='', editable=False, max_length=400)),
                ('dicofre', models.CharField(default='', editable=False, max_length=10)),
                ('poly', models.TextField(default='')),
                ('viewBox', models.CharField(default='', max_length=80)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacao', models.CharField(default='', editable=False, max_length=400)),
                ('dicofre', models.CharField(default='', editable=False, max_length=10)),
                ('poly', models.TextField(default='')),
                ('viewBox', models.CharField(default='', max_length=80)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacao', models.CharField(default='', max_length=400)),
                ('latitude', models.CharField(blank=True, default='', max_length=80)),
                ('longitude', models.CharField(blank=True, default='', max_length=80)),
                ('geocode', models.TextField(blank=True, default='')),
                ('geocode2', models.TextField(blank=True, default='')),
                ('geocode3', models.TextField(blank=True, default='')),
                ('concelho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flatmap.council')),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flatmap.district')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='', max_length=500)),
                ('texto', models.TextField(blank=True, default='')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('invertido', models.BooleanField(default=False)),
                ('imagem', models.ImageField(blank=True, upload_to='article/%Y/%m/%d')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='', max_length=500)),
                ('texto', models.TextField(blank=True, default='')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('invertido', models.BooleanField(default=False)),
                ('imagem', models.ImageField(blank=True, upload_to='article/%Y/%m/%d')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='', max_length=500)),
                ('texto', models.TextField(blank=True, default='')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('invertido', models.BooleanField(default=False)),
                ('imagem', models.ImageField(blank=True, upload_to='article/%Y/%m/%d')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=80)),
                ('link', models.URLField(default='', max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacao', models.CharField(default='', editable=False, max_length=400)),
                ('dicofre', models.CharField(default='', editable=False, max_length=10)),
                ('poly', models.TextField(default='')),
                ('viewBox', models.CharField(default='', max_length=80)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('concelho', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='flatmap.council')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacao', models.CharField(default='', max_length=400)),
                ('juridica', models.CharField(default='', max_length=100)),
                ('ano', models.IntegerField(default=0)),
                ('nipc', models.CharField(default='', max_length=9)),
                ('sede', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flatmap.equipment')),
                ('tags', models.ManyToManyField(to='flatmap.tag')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='freguesia',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='flatmap.parish'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flatmap.institution'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='morada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flatmap.address'),
        ),
        migrations.AddField(
            model_name='council',
            name='distrito',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='flatmap.district'),
        ),
    ]