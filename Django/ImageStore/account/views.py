from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class register_api(APIView):
    def post(self, request):
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        email = request.data.get('email')
        print("VIEWS: ", username, password1, password2, email)

        if not username or not email or not password2 or not password1:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'User with this username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if password1 == password2:

            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'token': access_token}, status=status.HTTP_201_CREATED)


def login_view(request):
    return render(request, 'account/login.html')


def register_view(request):
    print("TEST")
    return render(request, 'account/registration.html')


def logout_view(request):
    logout(request)
    return redirect('imageStoreApp:home')


@api_view(['POST'])
def login_api(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         user.set_password(request.data['password'])
#         user.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "user": serializer.data})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))