from django.utils.text import slugify

def generate_unique_slug(_class, field_name, from_field_name, instance):
    initial_slug = slugify(getattr(instance, from_field_name))
    unique_slug = initial_slug
    numb = 0
    while numb == 0 or matches.exists():
        matches = _class.objects.filter(**{field_name: unique_slug})
        if instance.pk:
            matches = matches.exclude(pk=instance.pk)

        numb += 1
        if matches.exists():
            unique_slug = f'{initial_slug}-{numb}'

    return unique_slug
