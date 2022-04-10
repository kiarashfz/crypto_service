from django.views.generic import FormView

from one_min_price.forms import CryptoPriceChooserForm


class Index(FormView):
    template_name = 'crypto-chooser.html'
    form_class = CryptoPriceChooserForm
