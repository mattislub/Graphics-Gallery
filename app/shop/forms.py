from django import forms  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore


class EarningFilterForm(forms.Form):
    date_from = forms.DateField(label=_('Date from'))
    date_to = forms.DateField(label=_('Date to'))
    income_type = forms.ChoiceField(choices=[('all', _('All')), ('balance_replenishments', _('Balance replenishments')), ('purchases', _('Purchases')), ('subscriptions', _('Subscriptions'))], label=_('Income type'))
