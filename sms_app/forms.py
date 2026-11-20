import re
from django import forms

class SMSForm(forms.Form):
    recipient = forms.CharField(
        label="Recipient Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567',
            'id': 'recipientInput',
        }),
        error_messages={'required': 'Please enter a recipient phone number.'}
    )
    message = forms.CharField(
        label="Message",
        max_length=1600,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your SMS message here...',
            'id': 'messageInput',
        }),
        error_messages={'required': 'Message cannot be empty.'}
    )

    def clean_recipient(self):
        phone = self.cleaned_data.get('recipient', '').strip()
        if not re.match(r'^\+[1-9]\d{7,14}$', phone):
            raise forms.ValidationError(
                "Invalid phone number format. Use E.164 format with country code (e.g., +639171234567)."
            )
        return phone

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if not msg:
            raise forms.ValidationError("Message cannot be empty or just spaces.")
        return msg