from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
    path('accounts/', include('allauth.urls')),
]
