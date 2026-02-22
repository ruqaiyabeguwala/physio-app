from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0002_exercise_external_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "kind",
                    models.CharField(
                        choices=[("visit", "Visit payment"), ("due_clear", "Due clear")],
                        max_length=20,
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        blank=True,
                        choices=[("upi", "UPI"), ("cash", "Cash"), ("other", "Other")],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "visit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="clinic.visit",
                    ),
                ),
            ],
        ),
    ]

