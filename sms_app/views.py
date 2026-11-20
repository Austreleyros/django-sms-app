import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SMSForm
from .models import SMSLog

TEXTBEE_SEND_URL = "https://api.textbee.dev/api/v1/gateway/send-sms"

def send_sms_view(request):
    if request.method == 'POST':
        form = SMSForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            message_body = form.cleaned_data['message']

            api_key = settings.TEXTBEE_API_KEY

            if not api_key:
                error_msg = "SMS service is not properly configured. Missing API credentials."
                SMSLog.objects.create(
                    recipient=recipient,
                    message_body=message_body,
                    status='Failed',
                    error_detail=error_msg
                )
                messages.error(request, error_msg)
                return redirect('send_sms')

            try:
                response = requests.post(
                    TEXTBEE_SEND_URL,
                    json={"recipients": [recipient], "message": message_body},
                    headers={"x-api-key": api_key, "Content-Type": "application/json"},
                    timeout=30,
                )

                if response.ok:
                    data = response.json().get("data", {})
                    batch_id = data.get("smsBatchId", "N/A")

                    SMSLog.objects.create(
                        recipient=recipient,
                        message_body=message_body,
                        status='Submitted',
                        provider_sid=batch_id
                    )

                    messages.success(
                        request,
                        f"SMS successfully submitted to TextBee (Batch ID: {batch_id}). "
                        "Note: Submission confirms the message is queued for your gateway device, not final handset delivery."
                    )
                    return redirect('send_sms')
                else:
                    try:
                        err_json = response.json()
                        err_msg = err_json.get("message") or err_json.get("error") or response.text
                    except ValueError:
                        err_msg = f"HTTP {response.status_code}"

                    safe_error = f"Provider rejected the request (Status {response.status_code}): {err_msg}"
                    SMSLog.objects.create(
                        recipient=recipient,
                        message_body=message_body,
                        status='Failed',
                        error_detail=safe_error
                    )
                    messages.error(request, safe_error)

            except requests.exceptions.RequestException:
                safe_error = "A network or connection error occurred while contacting the SMS provider."
                SMSLog.objects.create(
                    recipient=recipient,
                    message_body=message_body,
                    status='Failed',
                    error_detail=safe_error
                )
                messages.error(request, safe_error)
        else:
            messages.error(request, "Please correct the validation errors below.")
    else:
        form = SMSForm()

    logs = SMSLog.objects.all()[:15]
    return render(request, 'sms_app/index.html', {'form': form, 'logs': logs})