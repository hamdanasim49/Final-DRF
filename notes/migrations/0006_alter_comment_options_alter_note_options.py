# Generated by Django 4.1 on 2022-09-12 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0005_alter_comment_note"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["id"]},
        ),
        migrations.AlterModelOptions(
            name="note",
            options={"ordering": ["id"]},
        ),
    ]
