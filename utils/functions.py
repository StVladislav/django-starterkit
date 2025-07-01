from transliterate import slugify as _slugify


def slugify(char, model=None, field_name="slug"):
    """
    Function for slugify. It can add number at the end of a slug if its exists.

    char: str - slugified text
    model: django.db.models.Model
    field_name: field name of the model
    """
    slug = _slugify(char, language_code='uk')

    if not model:
        return slug
    
    _slug = slug
    counter = 0
    manager = model._default_manager
    field_filter = {f"{field_name}": _slug}

    while manager.filter(**field_filter).exists():
        counter += 1
        _slug = f"{slug}-{counter}"
        field_filter = {f"{field_name}": _slug}

    if counter:
        slug = f"{slug}-{counter}"
    
    return slug


