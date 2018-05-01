from django import template


register = template.Library()


@register.filter
def imdb_rating_color(rating):
    result = ''
    try:
        rating = float(rating)
        if isinstance(rating, float):
            if rating <= 4.0:
                result = 'imgb-rating-low'
            elif rating >= 5.0 and rating < 7.0:
                result = 'imgb-rating-medium'
            elif rating >= 7.0:
                result = 'imdb-rating-high'
    except:
        pass
    return result
