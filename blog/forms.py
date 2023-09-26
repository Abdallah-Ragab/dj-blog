from django.forms import Form, CharField, EmailField

class ShareViaEmailForm(Form):
    sender_name = CharField(max_length=25, required=True)
    sender_email = EmailField(required=True)
    receiver_email = EmailField(required=True)

class CommentForm(Form):
    name = CharField(max_length=50, required=True)
    email = EmailField(required=True)
    content = CharField(max_length=500, required=True)
