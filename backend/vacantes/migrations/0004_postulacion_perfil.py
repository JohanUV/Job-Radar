import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacantes", "0003_borradorcarta"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="postulacion",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="postulacion",
            name="usuario",
        ),
        migrations.AddField(
            model_name="postulacion",
            name="perfil",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="postulaciones",
                to="vacantes.perfilbusqueda",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="postulacion",
            name="estado",
            field=models.CharField(
                choices=[
                    ("guardada", "Guardada"),
                    ("postulada", "Postulada"),
                    ("entrevista", "Entrevista"),
                    ("oferta", "Oferta"),
                    ("rechazada", "Rechazada"),
                ],
                default="guardada",
                max_length=20,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="postulacion",
            unique_together={("vacante", "perfil")},
        ),
    ]
