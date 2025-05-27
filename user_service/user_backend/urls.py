
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import RegisterViewset, LoginViewset, MagiclinkLoginViewset, MeViewset

router = DefaultRouter()
router.register("register", RegisterViewset, basename="register")
router.register("login", LoginViewset, basename="login")
router.register("magic-link", MagiclinkLoginViewset, basename="magic-link-verify")

router.register("me", MeViewset, basename="me")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include(router.urls), name="userurls"),


    path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('allauth.socialaccount.urls')),

]
