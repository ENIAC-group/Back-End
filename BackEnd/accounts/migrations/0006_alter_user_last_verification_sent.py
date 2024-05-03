

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_last_verification_sent'),
    ]

    operations = [
        migrations.AlterField(

            model_name="user",
            name="last_verification_sent",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2024, 5, 3, 16, 26, 7, 6296),
                null=True,
            ),

        ),
    ]
