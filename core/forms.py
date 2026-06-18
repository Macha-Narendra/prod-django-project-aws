from decimal import Decimal

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Product


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = self._merge_css(widget, 'form-check-input')
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = self._merge_css(widget, 'form-select')
            else:
                widget.attrs['class'] = self._merge_css(widget, 'form-control')

            if field.required:
                widget.attrs.setdefault('aria-required', 'true')

    @staticmethod
    def _merge_css(widget, css_class):
        classes = widget.attrs.get('class', '').split()
        if css_class not in classes:
            classes.append(css_class)
        return ' '.join(classes)


class UserLoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'autofocus': True})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username', 'autofocus': True}),
        }


class ProductForm(BootstrapFormMixin, forms.ModelForm):
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'inputmode': 'decimal', 'min': '0.01', 'step': '0.01'}),
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'active': forms.CheckboxInput(attrs={'role': 'switch'}),
        }
