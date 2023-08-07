from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Lower
from django.shortcuts import render

from django.contrib.auth import login
from django_rest_passwordreset.views import ResetPasswordRequestToken
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        result = super(LoginAPI, self).post(request, format=None)

        return Response({**result.data, "role": user.role}, status=result.status_code)


class CheckAuthentication(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            # If the user is authenticated, return a 200 status code
            return Response({'detail': 'Authenticated', "first_name": user.first_name, "last_name": user.last_name, "role": user.role}, status=200)
        except Exception:
            # If the token is not valid, log out the user and return a 401 status code
            LogoutView.as_view()(request._request)
            return Response({'detail': 'Invalid token. Please log in again.'}, status=401)


class UsersApiView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            users = CustomUser.objects.all().order_by(Lower('first_name'))
            serializer = UserSerializer(users, many=True)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)


class UserApiDetailView(APIView):
    authentication_classes = [KnoxTokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            curr_user = request.user
            if curr_user.role == 1:
                user = CustomUser.objects.get(pk=pk)
                serializer = UserSerializer(user, many=False)
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'msg': "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response({'status': 'success', 'data': []}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'status': 'failed', 'data': []}, status=status.HTTP_404_NOT_FOUND)


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        # Call the parent's post method to execute the original functionality
        return super().post(request, *args, **kwargs)