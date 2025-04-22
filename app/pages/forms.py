from django import forms  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore


class ToSVGForm(forms.Form):
    file = forms.FileField(
        label=_('Drop file here or Select file'),
        widget=forms.FileInput(attrs={
            'accept': '.jpeg,.jpg,.png,.gif',
            'class': 'w-full',
        }),
        required=False,
    )

    file_path = forms.CharField(widget=forms.HiddenInput(), required=False)

    color_mode = forms.ChoiceField(
        choices=(
            ('color', _('Color')),
            ('binary', _('B&W')),
        ),
        initial='color',
        label=_('Color mode'),
        widget=forms.RadioSelect(
            attrs={
                'x-model': 'color_mode',
            },
        ),
    )

    mode = forms.ChoiceField(
        choices=(
            ('none', _('Pixel')),
            ('polygon', _('Polygon')),
            ('spline', _('Spline')),
        ),
        initial='spline',
        label=_('Mode'),
        widget=forms.RadioSelect(
            attrs={
                'class': 'bg-white rounded-lg',
                'x-model': 'mode',
            },
        ),
    )

    filter_speckle = forms.IntegerField(
        min_value=0,
        max_value=128,
        initial=4,
        label=_('Filter Speckle (Cleaner)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '0',
            'max': '128',
            'step': '1',
            'value': '4',
            'x-model': 'filter_speckle',
        }),
    )

    color_precision = forms.IntegerField(
        min_value=1,
        max_value=8,
        initial=6,
        label=_('Color Precision (More accurate)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '1',
            'max': '8',
            'step': '1',
            'value': '6',
            'x-model': 'color_precision',
        }),
    )

    layer_difference = forms.IntegerField(
        min_value=0,
        max_value=128,
        initial=4,
        label=_('Gradient Step (Less layers)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '0',
            'max': '128',
            'step': '1',
            'value': '4',
            'x-model': 'layer_difference',
        }),
    )

    corner_threshold = forms.IntegerField(
        min_value=0,
        max_value=180,
        initial=180,
        label=_('Corner Threshold (Smoother)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '0',
            'max': '180',
            'step': '1',
            'value': '180',
            'x-model': 'corner_threshold',
        }),
    )

    length_threshold = forms.FloatField(
        min_value=3.5,
        max_value=100,
        initial=4.0,
        label=_('Segment Length (More coarse)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '3.5',
            'max': '100',
            'step': '0.5',
            'value': '4',
            'x-model': 'length_threshold',
        }),
    )

    splice_threshold = forms.IntegerField(
        min_value=0,
        max_value=180,
        initial=45,
        label=_('Splice Threshold (Less accurate)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '0',
            'max': '180',
            'step': '1',
            'value': '45',
            'x-model': 'splice_threshold',
        }),
    )

    path_precision = forms.IntegerField(
        min_value=0,
        max_value=16,
        initial=8,
        label=_('Path Precision (More digits)'),
        widget=forms.widgets.NumberInput(attrs={
            'type': 'range',
            'class': 'w-full',
            'min': '0',
            'max': '16',
            'step': '1',
            'value': '2',
            'x-model': 'path_precision',
        }),
    )
