from django.urls import path
from cold_email_gen_app.views import (
    login_view, 
    register_view, 
    add_client_details, 
    index_view, 
    logout_view, 
    manage_links_view,
    generate_email_view,
    send_email,
)
from django.contrib import admin

urlpatterns = [
    path('index/', index_view, name='index'),
    path('add_client/', add_client_details, name='add_client'),
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('manage-links/', manage_links_view, name='manage_links'),
    path('generate-email/', generate_email_view, name='generate_email'),  # URL for generating email
    path('send-email/', send_email, name='send_email'),
    
]
