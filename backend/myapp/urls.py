from django.urls import path
from . import views
# from .views import assign_card_to_section
urlpatterns = [
    path('api/create_admin/', views.create_admin, name='create_admin'), 
    path('api/remove_admin/', views.remove_admin, name='remove_admin'),
    path('login/', views.login, name='login'),  

    path('api/get_balance/', views.get_balance, name='get_balance'),
    path('api/get_admins_balance/', views.get_admins_balance, name='get_admins_balance'),
    path('api/get_users/', views.get_users, name='get_users'), 
    path('api/payin_api/', views.payin_api, name='payin_api'),  
    path('api/payout_api/', views.payout_api, name='payout_api'),  
    path('api/payin_query/', views.payin_query, name='payin_query'),  
    path('api/payout_query/', views.payout_query, name='payout_query'),  
    path('api/payin_callback/', views.payin_callback, name='payin_callback'),  
     

]