from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User_information, Items_Category
from rest_framework.authtoken.models import Token
from .serializers import customer_information, items,LoginSerializer,SignupSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            json_response = {'status': status.HTTP_201_CREATED}
            return Response(json_response, status=status.HTTP_201_CREATED)
        else:
            json_response = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
            return Response(json_response, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request,username=username,password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                    "username": username,
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {
                        "Token": token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid username or password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid username or password",
            "data": serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def list_details(request):
    if request.method == 'GET':
        category_list = User_information.objects.all()
        serialized_post_list = customer_information(category_list, many=True)
        return JsonResponse(serialized_post_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        post_add_serializer = customer_information(data=request_data)
        if post_add_serializer.is_valid():
            post_add_serializer.save()
            return JsonResponse(post_add_serializer.data, status=201)
        return JsonResponse(post_add_serializer.errors, status=400)
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
def information(request, passed_id):
    try:
        category_detail = User_information.objects.get(id=passed_id)
    except User_information.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serialized_post_details = customer_information(category_detail)
        return JsonResponse(serialized_post_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        post_add_serializer = customer_information(category_detail, data=request_data)
        if post_add_serializer.is_valid():
            post_add_serializer.save()
            return JsonResponse(post_add_serializer.data, status=200)
        return JsonResponse(post_add_serializer.errors, status=400)
    elif request.method == 'DELETE':
        category_detail.delete()
        return HttpResponse(status=204)

@csrf_exempt
def items_list(request):
    if request.method == 'GET':
        category_list = Items_Category.objects.all()
        serialized_post_list = items(category_list, many=True)
        return JsonResponse(serialized_post_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        post_add_serializer = items(data=request_data)
        if post_add_serializer.is_valid():
            post_add_serializer.save()
            return JsonResponse(post_add_serializer.data, status=201)
        return JsonResponse(post_add_serializer.errors, status=400)

@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def items_details(request, passed_id):
    try:
        category_detail = Items_Category.objects.get(id=passed_id)
    except Items_Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serialized_post_details = items(category_detail)
        return JsonResponse(serialized_post_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        post_add_serializer = items(category_detail, data=request_data)
        if post_add_serializer.is_valid():
            post_add_serializer.save()
            return JsonResponse(post_add_serializer.data, status=200)
        return JsonResponse(post_add_serializer.errors, status=400)
    elif request.method == 'DELETE':
        category_detail.delete()
        return HttpResponse(status=204)

@csrf_exempt
def restore_information(request, passed_id):
    try:
        category_detail = User_information.objects.get(id=passed_id, isDeleted=True)
    except User_information.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        category_detail.isDeleted = False
        category_detail.save()
        return HttpResponse(status=200)

@csrf_exempt
def deleted_list(request):
    if request.method == 'GET':
        deleted_records = User_information.objects.filter(isDeleted=True)
        serialized_deleted_records = customer_information(deleted_records, many=True)
        return JsonResponse(serialized_deleted_records.data, safe=False, status=200)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def move_to_deleted(request, passed_id):
    try:
        category_detail = User_information.objects.get(id=passed_id)
    except User_information.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'DELETE':
        category_detail.isDeleted = True
        category_detail.save()
        return HttpResponse(status=204)
