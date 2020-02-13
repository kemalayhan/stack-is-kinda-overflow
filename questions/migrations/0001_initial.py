# Generated by Django 2.2.7 on 2019-11-21 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('tag', models.CharField(choices=[('java', 'JAVA'), ('cpp', 'C++'), ('python', 'Python')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions_image')),
                ('question_rank', models.IntegerField(blank=True, default=0, max_length=1, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='answers_image')),
                ('answer_rank', models.IntegerField(blank=True, default=0, max_length=1, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to='questions.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
