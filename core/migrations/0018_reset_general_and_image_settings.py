from django.db import migrations


def reset_general_and_image_settings(apps, schema_editor):
    GeneralSetting = apps.get_model('core', 'GeneralSetting')
    ImageSetting = apps.get_model('core', 'ImageSetting')
    GeneralSetting.objects.all().delete()
    ImageSetting.objects.all().delete()


def noop_reverse(apps, schema_editor):
    # Data deletion is intentionally not reversible.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_skill_show_percentage'),
    ]

    operations = [
        migrations.RunPython(reset_general_and_image_settings, noop_reverse),
    ]
