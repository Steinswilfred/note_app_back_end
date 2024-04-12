# from django.urls import path
# from .views import list_details,information,items_details,items_list,restore_information,deleted_list
# # urlpatterns = [
# #     path('list_details',list_details),
# #     path('information/<int:passed_id>',information),
# #     path('item_list',items_list),
# #     path('items_details/<int:passed_id>',items_details),
# #     path('information/restore/<int:passed_id>/', restore_information, name='restore_information'),
# #     path('deleted-list/', deleted_list),
# # ]
from django.urls import path
from .views import (
    list_details,
    information,
    items_details,
    items_list,
    restore_information,
    deleted_list,
    move_to_deleted,


)
from . import views
urlpatterns = [
    path('list_details/', list_details),
    path('information/<int:passed_id>/', information),
    path('item_list/', items_list),
    path('items_details/<int:passed_id>/', items_details),
    path('information/restore/<int:passed_id>/', restore_information, name='restore_information'),
    path('deleted_list/', deleted_list),
    path('move_to_deleted/<int:passed_id>/', move_to_deleted, name='move_to_deleted'),
    path('user/login',views.LoginAPIView.as_view(),name='login'),
    path('user/signup',views.SignupAPIView.as_view(),name="user-signup"),
]
