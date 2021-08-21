from django.contrib import admin
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail.message import EmailMessage
from django.http.response import HttpResponse
from . forms2 import email_form
from .models import Student

queryset_capture=Student.objects.none()

@admin.action(description="Send email to selected students")
def send_email_admin_init(modeladmin, request, queryset):
    global queryset_capture 
    queryset_capture = queryset
    return redirect(reverse('email-form'))

def send_email_admin(request):#needs message and subject...
    global queryset_capture
    #return HttpResponse(f"here is a query_{queryset_capture.count()}_")
    if(request.method=="POST"):
        #if 'subject' in request.POST:
        form=email_form(request.POST)
        if form.is_valid():
            #Now the email will be sent to all recipients
            sender_email = form.data.get('sender') if 'sender' in request.POST else None
            str_sub = form.data.get('subject')
            str_msg = form.data.get('message')
            recipients=queryset_capture
            count_all = recipients.count()
            recipients = recipients.filter(email__isnull=False)
            count=recipients.count()
            to_emails = list(map(lambda x : x.email , recipients))

            email = EmailMessage(subject=str_sub,body=str_msg,to=to_emails)
            email.send();
            messages.success(request ,f'Email sent to {count}/{count_all} addresses')
            #return back to the admin->student page...
            return redirect('/admin/records/student/')
    form = email_form()
    context={"form":form}
    #return email subject and message page...
    return render(request, "admin/emailform_aL_.html",context)