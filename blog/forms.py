from django.forms import Form, CharField, EmailField

class ShareViaEmailForm(Form):
    sender_name = CharField(max_length=25, required=True)
    sender_email = EmailField(required=True)
    receiver_email = EmailField(required=True)
