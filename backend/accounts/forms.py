from allauth.socialaccount.forms import SignupForm
from django import forms

class CustomSocialSignupForm(SignupForm):
    birth_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def save(self, request):
        user = super().save(request)
        user.birth_date = self.cleaned_data['birth_date']
        user.save()
        return user
