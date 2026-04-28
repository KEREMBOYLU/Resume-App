from django.db import migrations, models


def create_default_site_preference(apps, schema_editor):
    SitePreference = apps.get_model('core', 'SitePreference')
    SitePreference.objects.get_or_create(pk=1, defaults={'default_journey_tab': 'education'})


def delete_default_site_preference(apps, schema_editor):
    SitePreference = apps.get_model('core', 'SitePreference')
    SitePreference.objects.filter(pk=1, default_journey_tab='education').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_skill_percentage_remove_skill_show_percentage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('default_journey_tab', models.CharField(choices=[('experience', 'Experience'), ('education', 'Education')], default='education', help_text='Controls which Journey tab is open when the home page first loads.', max_length=20, verbose_name='Default journey tab')),
            ],
            options={
                'verbose_name': 'Site Preferences',
                'verbose_name_plural': 'Site Preferences',
            },
        ),
        migrations.RunPython(create_default_site_preference, delete_default_site_preference),
    ]
