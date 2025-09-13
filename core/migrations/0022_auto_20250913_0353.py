from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20250913_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='cliente',
            field=models.ForeignKey(
                to='core.Cliente',
                on_delete=models.CASCADE,
                related_name='pagamentos',
                default=1  # escolha um cliente existente para registros já salvos
            ),
        ),
    ]
