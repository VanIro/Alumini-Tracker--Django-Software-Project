from institutuff.models import Institute
from records.models import Student
from institutuff.filters import StudentFilter

from django.shortcuts import render
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.core.mail.message import EmailMessage

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator



# Create your views here.
def institute_login(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data.get('userName'), password=form.data.get('password'))
            if user is not None:
                login(request,user)
                return HttpResponseRedirect (reverse('institute-logged-in'))
            else:
                messages.warning(request, f'Your username or password was incorrect')#later replace the message with the one below #more secure
        else:
            messages.warning(request, f'Record not found! Please check your input credentials properly')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'institutuff/institute_login.html', context)

def institute_logged_in(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect (reverse('institute-log-in'))
    #return HttpResponse("ynha aayo...")
    return view_alumni.as_view()(request)

    if request.method =='POST':
        return send_email(request,request.POST["list_recipients"],request.POST["subject"],request.POST["message"])

    admin_model = Institute.objects.get(userName = request.user)
    context={
        'admin_model':admin_model    
    }
    return render(request, 'institutuff/institute_list.html',context)

def logout_institute(request):
    logout(request)
    return HttpResponseRedirect (reverse('institute-log-in'))

def send_email(request, string, str_sub, str_msg):
    filters = string.split("::")
    filters = filters[:-1]
    hierarchy = ['year','level','program','group']
    recipients = Student.objects.all()
    if filters[1]=='bachelors':
        filters.pop(1)
        count =len(filters)
        if count>0:
            recipients = recipients.filter(be_batch_bs = filters[0])
            count-=1
        if count>0:
            recipients = recipients.filter(be_program = filters[1])
            count-=1
        if count>0:
            recipients = recipients.filter(be_student_group = filters[2])
    elif filters[1] == 'masters':
        pass    #...
    elif filters[1] == 'phd':
        pass    #...
    
    #Now the email will be sent to all recipients
    count_all = recipients.count()
    recipients = recipients.filter(email__isnull=False)
    count=recipients.count()
    to_emails = list(map(lambda x : x.email , recipients))

    email = EmailMessage(subject=str_sub,body=str_msg,to=to_emails)
    email.send();
    messages.success(request ,f'Email sent to {count}/{count_all} addresses')
    return HttpResponseRedirect(reverse('institute-logged-in'))
    #return HttpResponse(f'Email sent to {count}/{count_all} addresses')



class view_alumni(ListView):
    model=Student
    paginate_by = 17
    template_name = 'institutuff/alumniView.html'
    context_object_name = 'alumni'
    def __init__(self, *args, **kwargs):
        self.filter_form=None
        self.query_display = None
        #self.paginate_by = 1
        super(view_alumni,self).__init__(*args,**kwargs)

    def get_context_data(self, **kwargs):
        context=super(view_alumni,self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['query_display'] = self.query_display
        url_get_part = self.request.get_full_path().split("?")
        if len(url_get_part)<=1:
            url_get_part=[""]
        else:
            url_get_part=url_get_part[1].split("page")
            if len(url_get_part)>1:
                #if there are more get parameters after page(in future), but not used now
                url_get_part[1] = url_get_part[1].split('&',1)[-1]
            print(url_get_part)
            if len(url_get_part[0])>0 and (not url_get_part[0][-1] == '&') :
                url_get_part[0] = url_get_part[0]+'&'
          
        context['current_url_get'] = url_get_part[0]
        #context['filter'] = StudentFilter(self.request.GET, self.queryset)
        return context

    def get_queryset(self):
        queryset = Student.objects.filter()
        self.query_display = query_string(self.request.GET) 
        filter = StudentFilter(self.request.GET, queryset)
        #self.context['qrySet'] = filter.qs
        self.filter_form = filter.form
        return filter.qs#self.context['filter'].qs#Student.objects.filter()

    def get_paginator(self, queryset, per_page, **kwargs):
        #raise ValidationError(self.get_paginator()) #= Paginator(filter.qs,3)
        return super().get_paginator(queryset, per_page, **kwargs)
    #def get_context_data(self,*args,**kwargs):
    #    context=super().get_context_data(*args,**kwargs)
    #    context[]=institute.objects.all().order_by()
    #    return context

filter_categories = [
        "batch", "program","level","country"
    ]
def query_string(get_data):
    string = ""
    flag = False
    for fil in filter_categories:
        if fil in get_data and len(get_data[fil].strip()) > 0:
            flag = True
            string = string + fil + " : '" + get_data[fil] + "' , "

    if flag: 
        string = string[:-3]
        return string
    else : return None
