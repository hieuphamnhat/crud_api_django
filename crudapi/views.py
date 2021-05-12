from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import forms
from crudapi.forms import RegisterForm
from tdtDjangoAPi.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.models import User

@csrf_exempt
@api_view(['GET', 'POST'])
def company_list(request):
    if request.method == 'POST':
        try:
            company_data = JSONParser().parse(request)
            company_serializer = CompanySerializer(data=company_data)
            
            if company_serializer.is_valid():
                company_serializer.save()
                print(company_serializer.data)
                response = {
                'message': "Successfully Upload a Company with id = %d" % company_serializer.data.get('id'),
                'companies': [company_serializer.data],
                'error': "" 
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                error = {
                    'message':"Can Not upload successfully!",
                    'companies':"[]",
                    'error': company_serializer.errors
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        except: 
            exceptionError = {
                    'message': "Can Not upload successfully!",
                    'companies': "[]",
                    'error': "Having an exception!"
                }
        return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            companies = Company.objects.all()
            companies_serializer = CompanySerializer(companies, many=True)

            response = {
                'message': "Get all companies'Infos Successfully",
                'companies': companies_serializer.data,
                'error': ""
            }
            #return JsonResponse(response, status=status.HTTP_200_OK)
            return JsonResponse(companies_serializer.data, safe=False)
        except: 
            error = {
                'message': "Fail! -> can NOT get all the companies List. Please check again!",
                'companies': "[]",
                'error': "Error"
            }
            return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT', 'DELETE'])
def company_detail(request, pk):
    try: 
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        exceptionError = {
            'message': "Not found a companies with id = %s!" % pk,
            'companies': "[]",
            'error': "404 Code - Not Found!"
        }
        return JsonResponse(exceptionError, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'PUT':
        try:
            company_data = JSONParser().parse(request)
            company_serializer = CompanySerializer(company, data=company_data)

            if company_serializer.is_valid(): 
                company_serializer.save()
                response = {
                    'message': "Successfully Update a Company with id = %s" % pk,
                    'companies': [company_serializer.data],
                    'error': ""
                }                
                return JsonResponse(response) 

            response = {
                    'message': "Fail to Update a Company with id = %s" % pk,
                    'companies': [company_serializer.data],
                    'error': company_serializer.errors
                }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST) 
        except:
            exceptionError = {
                'message': "Fail to update a Company with id = %s!" % pk,
                'companies': [company_serializer.data],
                'error': "Internal Error!"
            }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    elif request.method == 'DELETE':
        print("Deleting a Company with id=%s"%pk)
        company.delete() 
        company_serializer = CompanySerializer(company) 
        response = {
                'message': "Successfully Delete a company with id = %s" % pk,
                'companies': [company_serializer.data],
                'error': ""
            }
        return JsonResponse(response)

def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'pwd123'
    return HttpResponse("<h1>dataflair<br> the session is set</h1>")

def access_session(request):
    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    if request.session.get('name'):
        response += "Name: {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password: {0} <br>".format(request.session.get('password'))
        return HttpResponse(response)
    else:
        return redirect('create/')

def delete_session(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")

#email
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to DataFlair'
        message = 'Hope you are enjoying my messages'
        recepient = str(sub['Email'].value())
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'crudapi/success.html', {'recepient': recepient})
    return render(request, 'crudapi/index.html', {'form':sub})

#register
class registerUser(View):
    def get(self, request):
        rf = RegisterForm()
        return render(request, 'crudapi/register.html', {'rf': rf})

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return HttpResponse("Regist successfully")
        