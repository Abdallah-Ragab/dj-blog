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


def get_list_of_pagination_pages(current_page, number_of_pages, list_length=5, insert_ellipsis=True):
    potential_before = [i for i in range(1, current_page) if i > 0]
    potential_after = [i for i in range(current_page + 1, number_of_pages + 1) if i > 0]

    chosen_before = potential_before[-int(list_length/2):]
    chosen_length = len(chosen_before)
    remaining_length = list_length - chosen_length - 1

    chosen_after = potential_after[:int(remaining_length)]
    pagination_list = chosen_before + [current_page] + chosen_after

    if insert_ellipsis:
        if pagination_list[0] != 1:
            _pagination_list = [1]
            if pagination_list[0] - 1 == 2:
                _pagination_list.append(2)
            elif pagination_list[0] - 1 > 2:
                _pagination_list.append('...')
            pagination_list = _pagination_list + pagination_list

        if pagination_list[-1] != number_of_pages:
            pagination_list_ = [number_of_pages]
            if number_of_pages - pagination_list[-1] == 2:
                pagination_list_.insert(-1, number_of_pages - 1)
            elif number_of_pages - pagination_list[-1] > 2:
                pagination_list_.insert(-1, '...')
            pagination_list = pagination_list + pagination_list_


    return pagination_list