from django import forms


def validate_integer_is_not_zero(value):
    if value is 0:
        raise forms.ValidationError(
            'You cannot have a Pokemon with id 0.'
        )
