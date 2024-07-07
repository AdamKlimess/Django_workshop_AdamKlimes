from django.urls import path
from .views import new_room, list_of_rooms, delete_room, modify_room, reservation, detail_view, search_rooms

urlpatterns = [
    path('room/new/', new_room, name='new_room'),
    path('room/list/', list_of_rooms, name='list_of_rooms'),
    path('room/delete/<int:room_id>/', delete_room, name='delete_room'),
    path('room/modify/<int:room_id>/', modify_room, name='modify_room'),
    path('room/reservation/<int:room_id>/', reservation, name='reservation'),
    path('room/detail/<int:room_id>/', detail_view, name='room_detail'),
    path('room/search/', search_rooms, name='search_room')
]
