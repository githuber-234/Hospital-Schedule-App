from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('Scheduler.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
