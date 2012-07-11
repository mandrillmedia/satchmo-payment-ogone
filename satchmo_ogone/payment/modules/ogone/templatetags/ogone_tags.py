from django import template
register = template.Library()

from django_ogone.ogone import Ogone

@register.simple_tag(takes_context=True)
def get_ogone_form(context):
    data = {}
    #transaction data
    data['PSPID'] = 'mypspid'
    data['orderID'] = '1'
    data['amount'] = '500'
    data['currency'] = 'EUR'
    data['language'] = 'en'
    context['form'] = Ogone.get_form(data)
    context['action'] = Ogone.get_action()

