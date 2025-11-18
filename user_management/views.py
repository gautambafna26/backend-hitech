from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ChangePasswordSerializer
from django.conf import settings
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    UserPermissionsSerializer,
    UserProfileSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "message": "Login successful",
                "token": access_token,  # Include token in response for debugging
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_active": user.is_active,
                }
            })
            
            # Set HTTP-only cookies with proper configuration
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                domain=None,
                path='/',
                max_age=7 * 24 * 60 * 60  # 7 days, matching SIMPLE_JWT settings
            )
            
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                domain=None,
                path='/',
                max_age=60 * 60  # 1 hour, matching SIMPLE_JWT settings
            )
            
            return response
            
        return Response(
            {"error": "Invalid credentials"}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # ✅ Mark token as blacklisted

            response = Response({"message": "Successfully logged out"})
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "No refresh token found"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            # Verify and create new refresh token
            refresh = RefreshToken(refresh_token)
            
            # If token rotation is enabled, blacklist the current token
            if getattr(settings, 'SIMPLE_JWT', {}).get('ROTATE_REFRESH_TOKENS', False):
                try:
                    # Blacklist current token
                    refresh.blacklist()
                except Exception:
                    pass
                
                # Get new tokens
                refresh = RefreshToken.for_user(request.user)
            
            response = Response({"message": "Token refreshed successfully"})
            
            # Set new refresh token if rotation is enabled
            if getattr(settings, 'SIMPLE_JWT', {}).get('ROTATE_REFRESH_TOKENS', False):
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    expires=None
                )
            
            # Set new access token
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                expires=None
            )
            return response
            
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get all permissions for the currently authenticated user
        """
        try:
            user = request.user
            serializer = UserPermissionsSerializer(user)
            
            return Response({
                'success': True,
                **serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------