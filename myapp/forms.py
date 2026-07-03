from django import forms
import re
from datetime import datetime

class DonationForm(forms.Form):
    # --- Existing Donor Info ---
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    amount = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'placeholder': 'Donation Amount (₹)', 'id': 'donation-amount'}))
    cause = forms.ChoiceField(choices=[
        ('', 'Select a Cause'),
        ('healthcare', 'Healthcare for Children'),
        ('education', 'Education for All'),
        ('poverty', 'Poverty Relief'),
        ('environment', 'Environmental Sustainability'),
    ])

    # --- Integrated Mock Payment Fields ---
    card_number = forms.CharField(
        max_length=19, # Supports spaces
        widget=forms.TextInput(attrs={'placeholder': 'Card Number (16 digits)', 'id': 'cc-number', 'autocomplete': 'cc-number'})
    )
    card_expiry = forms.CharField(
        max_length=5, # MM/YY formatting space wrapper
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY', 'id': 'cc-expiry', 'autocomplete': 'cc-exp'})
    )
    card_cvv = forms.CharField(
        max_length=4, 
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'CVV', 'id': 'cc-cvv', 'autocomplete': 'cc-csc'})
    )

    # Clean Validation: Checks card number format
    def clean_card_number(self):
        card_num = re.sub(r'\s+', '', self.cleaned_data.get('card_number', '')) # Remove spacing parameters
        if not card_num.isdigit() or len(card_num) < 13 or len(card_num) > 16:
            raise forms.ValidationError("Please provide a valid 13 to 16 digit card structural sequence.")
        return card_num

    # Clean Validation: Checks card date expiration constraints
    def clean_card_expiry(self):
        expiry = self.cleaned_data.get('card_expiry', '').strip()
        if not re.match(r'^(0[1-12]|1[0-2])\/[0-9]{2}$', expiry):
            raise forms.ValidationError("Format must perfectly match expiration signature layout: MM/YY.")
        
        # Calculate current time parameters for validity checks
        month, year = map(int, expiry.split('/'))
        current_year = int(str(datetime.now().year)[2:]) # Get two-digit target layout bounds
        current_month = datetime.now().month

        if year < current_year or (year == current_year and month < current_month):
            raise forms.ValidationError("This card has expired.")
        return expiry

    # Clean Validation: Structural CVV parameter check
    def clean_card_cvv(self):
        cvv = self.cleaned_data.get('card_cvv', '').strip()
        # FIXED: Added the required checking list [3, 4]
        if not cvv.isdigit() or len(cvv) not in[3, 4]:
            raise forms.ValidationError("CVV must be 3 or 4 digits.")
        return cvv


class VolunteerForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    interest = forms.ChoiceField(
        required=True,
        choices=[
            ('', 'Area of Interest'),
            ('education', 'Education Support'),
            ('medical', 'Medical Assistance'),
            ('food', 'Food Distribution'),
            ('event', 'Event Coordination'),
            ('remote', 'Online / Remote Volunteering'),
        ],
        widget=forms.Select(attrs={'class': 'select-dropdown'})
    )
    availability = forms.ChoiceField(
        required=True,
        choices=[
            ('', 'Availability'),
            ('weekdays', 'Weekdays'),
            ('weekends', 'Weekends'),
            ('flexible', 'Flexible / On-Call'),
        ],
        widget=forms.Select(attrs={'class': 'select-dropdown'})
    )