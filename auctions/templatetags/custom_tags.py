from django import template

register = template.Library()

@register.filter()
def get_auction_watchlist(value, arg):
    return value.filter(auction=arg)
