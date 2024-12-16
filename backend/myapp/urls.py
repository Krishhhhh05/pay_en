from django.urls import path
from . import views
# from .views import assign_card_to_section
urlpatterns = [
    path('api/get_balance/', views.get_balance, name='get_balance'),  
    path('api/payin_api/', views.payin_api, name='payin_api'),  
    path('api/payout_api/', views.payout_api, name='payout_api'),  
    path('api/payin_query/', views.payin_query, name='payin_query'),  
    path('api/payout_query/', views.payout_query, name='payout_query'),  
    path('api/payin_callback/', views.payin_callback, name='payin_callback'),  
     

]