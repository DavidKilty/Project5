
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_faq_created_at_faq_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
