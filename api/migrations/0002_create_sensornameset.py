from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("api", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="SensorNameSet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("device_id", models.CharField(max_length=50, unique=True)),
                ("t1_name", models.CharField(max_length=100, blank=True, default='T1')),
                ("h1_name", models.CharField(max_length=100, blank=True, default='H1')),
                ("t2_name", models.CharField(max_length=100, blank=True, default='T2')),
                ("h2_name", models.CharField(max_length=100, blank=True, default='H2')),
                ("t3_name", models.CharField(max_length=100, blank=True, default='T3')),
                ("h3_name", models.CharField(max_length=100, blank=True, default='H3')),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
