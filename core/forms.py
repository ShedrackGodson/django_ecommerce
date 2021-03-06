from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



PAYMENT_OPTION = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "123 Mount St", "class": "form-control"
    }))
    appartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "placeholder": "Appartment or suite", "class": "form-control"
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            "class": "form-control"
        })
    )
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_OPTION)
