
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_last_verification_sent"),
    ]

    operations = [
        migrations.AlterField(

            model_name='user',
            name='last_verification_sent',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 8, 13, 42, 48, 339082), null=True),
            name="last_verification_sent",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2024, 4, 19, 14, 26, 53, 742775),
                null=True,
            ),

        ),
    ]
