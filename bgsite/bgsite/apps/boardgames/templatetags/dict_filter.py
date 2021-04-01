from django.template.defaulttags import register

@register.filter
def get_shop_link(all_db_bg, key):
    key = key.lower()
    for bg in all_db_bg:
        if bg.get(key):
            return bg.get(key)

@register.filter
def get_ru_name(all_db_bg, key):
    key = key.lower()
    for bg in all_db_bg:
        if bg.get(key):
            return bg.get("ru_name")