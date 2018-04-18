from django import template


register = template.Library()

@register.filter
def month_ukrainian(date):
    print(date)
    monthDict = {0: 'грудень', 1: 'січень', 2: 'лютий', 3: 'березень', 4: 'квітень',
                 5: 'травень', 6: 'червень', 7: 'липень', 8: 'серпень',
                 9: 'вересень', 10: 'жовтень', 11: 'листопад', 12: 'грудень'}
    return (monthDict[date.month]+','+str(date.year))
