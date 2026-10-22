from django.db import migrations


def add_astar_algorithm(apps, schema_editor):
    Algorithm = apps.get_model("app", "Algorithm")
    Algorithm.objects.get_or_create(name="A* Search Algorithm")


def remove_astar_algorithm(apps, schema_editor):
    Algorithm = apps.get_model("app", "Algorithm")
    Algorithm.objects.filter(name="A* Search Algorithm").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_astar_algorithm, remove_astar_algorithm),
    ]
