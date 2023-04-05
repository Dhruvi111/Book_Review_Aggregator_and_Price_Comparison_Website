# from django import forms
# from .models import UserReview, RATE_CHOICES

# class RateForm(forms.Modelform):
#     reviewText = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
#     rating = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

#     class Meta:
#         model = UserReview
#         fields = ('reviewText', 'rating')