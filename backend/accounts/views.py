from .account_serializer import AccountSerializer
from .models import Account
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

def get_refresh_token(user):

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def index(request):
    return HttpResponse('index')

class AuthView(CreateAPIView):

    def post(self, request):

        account_serializer = AccountSerializer(data=request.data)
        account_serializer.is_valid(raise_exception=True)
        user = account_serializer.save()

        return Response(data=get_refresh_token(user))

class AuthUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = Account.objects.filter(email=request.data['email']).first()
        if user:
            query = AccountSerializer(user)
            return_data = query.data
            return_status = status.HTTP_200_OK
        else:
            return_data = {'error': 'User Not Found'}
            return_status = status.HTTP_404_NOT_FOUND
        
        return Response(return_data, status=return_status)
        

    def patch(self, request):

        account_serializer = AccountSerializer(request.user, data=request.data, partial=True)
        account_serializer.is_valid(raise_exception=True)
        account_serializer.save()

        return Response(account_serializer.data)

    def delete(self, request):
        user = Account.objects.filter(email=request.data['email']).first()

        if user:
            user.delete()
            return_data = {'data': 'User deleted'}
            return_status = status.HTTP_410_GONE
        else:
            return_data = {'error': 'User Not Found'}
            return_status = status.HTTP_404_NOT_FOUND

        return Response(return_data, status=return_status)
    
class AuthOwnUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = AccountSerializer

    def get(self, request):

        user = self.serializer_class(request.user)
        return_data = {
            'id': user.data['id'],
            'full_name': user.data['full_name'],
            'email': user.data['email']
        }
        return Response(return_data)
    
    def patch(self, request):

        account_serializer = AccountSerializer(request.user)
        user = account_serializer.update(instance=request.user, validated_data=request.data)
        
        return Response(data=get_refresh_token(user))
    
    def delete(self, request):

        user = Account.objects.filter(id=request.user.id).first()
        if user:
            user.delete()
            return_data = {'data': 'User deleted'}
            return_status = status.HTTP_410_GONE
        else:
            return_data = {'error': 'User Not Found'}
            return_status = status.HTTP_404_NOT_FOUND

        return Response(return_data, status=return_status)