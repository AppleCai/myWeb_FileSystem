# Generated by Django 2.2.5 on 2019-10-03 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicinfo',
            name='FileID',
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='status',
            field=models.IntegerField(choices=[(0, 'opencv'), (1, 'python'), (2, 'c++'), (3, 'ROS'), (4, 'Linux'), (5, '计算机视觉'), (6, '机器学习'), (7, 'Django'), (8, '数学算法')], default=0, help_text='选择类型', verbose_name='归类'),
        ),
        migrations.AlterField(
            model_name='basicinfo',
            name='tag_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
