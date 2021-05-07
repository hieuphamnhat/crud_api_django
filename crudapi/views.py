from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
