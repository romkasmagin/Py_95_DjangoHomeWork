import django

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'work_stream_project.settings')
django.setup()


from work_stream.models import Tag
from users.models import Skill
from faker import Faker


fake = Faker()

for _ in range(10):
    tag_data = {
        'name': fake.word(),
        'slug': fake.slug(),
        'created': fake.date(),
    }

    Tag.objects.create(**tag_data)


for _ in range(10):
    skill_data = {
        'name': fake.word(),
        'slug': fake.slug(),
        'description': fake.text(max_nb_chars=200),
        'created': fake.date(),
    }

    Skill.objects.create(**skill_data)


