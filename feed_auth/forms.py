from django import forms

from freefeeds.client import Client


class AuthForm(forms.Form):
    api_key = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super().clean()

        try:
            api_client = Client(cleaned_data["api_key"])
            if api_client.get_me() is not None:
                return cleaned_data
            else:
                self.add_error('api_key', "Looks like the token is invalid, please check it and try again")
        except Exception as e:
            self.add_error('api_key', "Looks like the token is invalid, please check it and try again")
