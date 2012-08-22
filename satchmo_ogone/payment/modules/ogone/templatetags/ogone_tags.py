from django import template
register = template.Library()

from django_ogone.ogone import Ogone
from django.contrib.sites.models import Site
from django.core import urlresolvers
from livesettings import config_get_group, config_value

#TODO: same functions as used in views, perhaps generalize them
#had trouble reusing from the views models itself
def reverse_full_url(view, *args, **kwargs):
    current_site = Site.objects.get_current()
    protocol = kwargs.pop('secure', False) and 'https' or 'http'
    
    relative_url = urlresolvers.reverse(view, *args, **kwargs)
    
    return '%s://%s%s' % (protocol, current_site.domain, relative_url)

def get_ogone_settings():
    payment_module = config_get_group('PAYMENT_OGONE')

    class Settings(object):
        SHA_PRE_SECRET = payment_module.SHA_PRE_SECRET.value
        SHA_POST_SECRET = payment_module.SHA_POST_SECRET.value
        HASH_METHOD = payment_module.HASH_METHOD.value
        PRODUCTION = payment_module.LIVE.value
        PSPID = payment_module.PSPID.value
        CURRENCY = payment_module.CURRENCY_CODE.value
        TEST_URL = payment_module.TEST_URL.value
        PROD_URL = payment_module.PROD_URL.value
        
    return Settings

@register.simple_tag(takes_context=True)
def get_ogone_form(context):
    data = {}
    #transaction data
    #data['PSPID'] = 'mypspid'
    settings = get_ogone_settings()
    order = context['order']
    data['orderID'] = order.pk
    data['amount'] = ("%.2f" % order.total).replace(".","")
    data['currency'] = settings.CURRENCY
    data['language'] = getattr(context['request'], 'LANGUAGE_CODE', 'en_US')
    s="""
    context['success_url'] = reverse_full_url('OGONE_satchmo_checkout-success')
    context['failure_url'] = reverse_full_url('OGONE_satchmo_checkout-failure')
    context['homeurl'] = reverse_full_url('satchmo_shop_home')
    """
    context['catalogurl'] = reverse_full_url('satchmo_category_index')
    context['form'] = Ogone.get_form(data)
    context['action'] = Ogone.get_action()

