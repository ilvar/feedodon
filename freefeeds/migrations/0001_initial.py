# Generated by Django 3.0 on 2019-12-14 20:57

from django.db import migrations, models
import django.db.models.deletion
import freefeeds.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.CharField(db_index=True, max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('screen_name', models.CharField(max_length=100)),
                ('avatar_url', models.URLField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            bases=(models.Model, freefeeds.models.FfToMdConvertorMixin),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.CharField(db_index=True, max_length=100)),
                ('body', models.TextField()),
                ('comment_likes', models.IntegerField()),
                ('comments_disabled', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='freefeeds.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freefeeds.User')),
            ],
            bases=(models.Model, freefeeds.models.FfToMdConvertorMixin),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.CharField(db_index=True, max_length=100)),
                ('media_type', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=256)),
                ('thumbnail_url', models.CharField(max_length=256)),
                ('width', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freefeeds.Post')),
            ],
            bases=(models.Model, freefeeds.models.FfToMdConvertorMixin),
        ),
    ]
