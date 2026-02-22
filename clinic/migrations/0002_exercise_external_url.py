from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="external_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="exercise",
            name="google_drive_file_id",
            field=models.CharField(max_length=255, blank=True),
        ),
    ]

