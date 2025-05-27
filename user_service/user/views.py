from django.shortcuts import render
from .serializer import RegisterSerializer, LoginSerializer, MagicLinkRequestSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated



class RegisterViewset(viewsets.ModelViewSet):

    http_method_names = ['post']
    serializer_class = RegisterSerializer
    lookup_field = "username"
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            
            return Response(
                {
                    "user": serializer.data,
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token)
                }, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewset(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    http_method_names = ['post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data

        return Response(
            {
                'user': str(validated_data.get("user")),
                'refresh_token': validated_data.get("refresh_token"),
                'access_token': validated_data.get("access_token"),
                'message': validated_data.get("message", None)
            }
        )

class MagiclinkLoginViewset(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = MagicLinkRequestSerializer
    http_method_names = ["post"]  # Only allow POST for both endpoints

    def create(self, requset, *args, **kwargs):
        serializer = self.get_serializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)


from .serializer import UserSerializer
from rest_framework.decorators import action


class MeViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)