from django.db import migrations
from django.utils import timezone


def backfill_payments(apps, schema_editor):
    Visit = apps.get_model("clinic", "Visit")
    Payment = apps.get_model("clinic", "Payment")

    visits = Visit.objects.filter(is_deleted=False).exclude(amount_paid=0)
    for visit in visits.iterator():
        if Payment.objects.filter(visit=visit, kind="visit").exists():
            continue
        created_at = visit.payment_date or visit.created_at
        if not created_at:
            created_at = timezone.now()
        Payment.objects.create(
            visit=visit,
            amount=visit.amount_paid,
            kind="visit",
            method=visit.payment_method,
            created_at=created_at,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0003_payment"),
    ]

    operations = [
        migrations.RunPython(backfill_payments, migrations.RunPython.noop),
    ]

