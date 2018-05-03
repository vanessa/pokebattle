from django import forms


def validate_integer_doesnt_start_with_zero(value):
    if str(value).startswith('0'):
        raise forms.ValidationError(
            'Your Pokemon id ({pokemon_id}) cannot start with 0.'.format(
                pokemon_id=value
            )
        )
