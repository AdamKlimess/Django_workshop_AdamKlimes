from datetime import date, datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Room, RoomReservation


# Create your views here.


def new_room(request):
    error_message = []
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        projector_availability = request.POST.getlist('projector_availability')
        print(projector_availability, room_capacity, room_name)
        if "on" in projector_availability:
            projector_availability_boolean = True
        else:
            projector_availability_boolean = False
        try:
            if not room_name:
                error_message.append("Room name cannot be empty")
            if Room.objects.filter(room_name=room_name).exists():
                error_message.append("Room already exists")
            if not room_capacity.isdigit():
                error_message.append("Room capacity must be an integer")
            else:
                room = Room(room_name=room_name, room_capacity=room_capacity,
                            projector_availability=projector_availability_boolean)
                room.save()
                return render(request, 'booking_manager/new_room.html',
                              context={'room_name': room_name, 'room_capacity': room_capacity,
                                       'projector_availability': projector_availability})

        except ValueError:
            error_message.append("Invalid input")
            return render(request, 'booking_manager/new_room.html',
                          context={'error_message': error_message})
    return render(request, 'booking_manager/new_room.html',
                  context={'error_message': error_message})


def list_of_rooms(request):
    rooms = Room.objects.all()
    for room in rooms:
        if room.reservations.filter(date=date.today()).exists():
            room.room_availability = False
        else:
            room.room_availability = True
    if not rooms:
        return render(request, 'booking_manager/no_rooms.html')
    return render(request, 'booking_manager/list_of_rooms.html', context={'rooms': rooms})


def delete_room(request, room_id):
    rooms = Room.objects.all()
    room = Room.objects.get(id=room_id)
    room.delete()
    return render(request, 'booking_manager/list_of_rooms.html', context={'rooms': rooms})


def modify_room(request, room_id):
    error_message = []
    if request.method == 'GET':
        room = Room.objects.get(id=room_id)
        return render(request, 'booking_manager/modify_room.html', context={'room': room})

    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        projector_availability = request.POST.getlist('projector_availability')
        print(projector_availability, room_capacity, room_name)
        if "on" in projector_availability:
            projector_availability_boolean = True
        else:
            projector_availability_boolean = False
        try:
            if not room_name:
                error_message.append("Room name cannot be empty")
            if not room_capacity.isdigit():
                error_message.append("Room capacity must be an integer")
            else:
                room = Room.objects.get(id=room_id)
                room.room_name = room_name
                room.room_capacity = room_capacity
                room.projector_availability = projector_availability_boolean
                room.save()
                return render(request, 'booking_manager/list_of_rooms.html',
                              context={'room_name': room_name, 'room_capacity': room_capacity,
                                       'projector_availability': projector_availability,
                                       'room_id': room_id})

        except ValueError:
            error_message.append("Invalid input")
            return render(request, 'booking_manager/new_room.html',
                          context={'error_message': error_message})
    return render(request, 'booking_manager/new_room.html',
                  context={'error_message': error_message})


def reservation(request, room_id):
    reservation = RoomReservation.objects.filter(room_id=room_id).order_by('date')
    room = Room.objects.get(id=room_id)
    error_message = []
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)
        print(room.room_name)
        comment = request.POST.get('comment')
        reservation_date_str = request.POST.get('reservation_date')
        print(reservation_date_str)
        if not reservation_date_str:
            error_message.append("Please select a date.")
            return render(request, 'booking_manager/reservation.html',
                          context={'error_message': error_message, 'room': room, 'reservation': reservation})
        reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
        print(reservation_date)

        existing_reservations = RoomReservation.objects.filter(room_id=room_id, date=reservation_date)
        if existing_reservations.exists():
            error_message.append("This room is already booked on the selected date.")

        today = date.today()
        if reservation_date < today:
            error_message.append("Selected date is in the past.")

        if not error_message:
            reservation = RoomReservation(date=reservation_date, room_id_id=room_id, comment=comment)
            reservation.save()

            return redirect('list_of_rooms')

    return render(request, 'booking_manager/reservation.html',
                  context={'room': room, 'error_message': error_message, 'reservation': reservation})


def detail_view(request, room_id):
    room = Room.objects.get(id=room_id)
    reservation = RoomReservation.objects.filter(room_id=room_id).order_by('date')
    return render(request, 'booking_manager/room_detail.html',
                  context={'room': room, 'reservation': reservation})


def search_rooms(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        capacity = request.POST.get('capacity')
        projector = request.POST.getlist('projector')
        print(projector, capacity, room_name)
        if "on" in projector:
            projector_boolean = True
        else:
            projector_boolean = False
        if room_name:
            rooms = rooms.filter(room_name__icontains=room_name)
            return render(request, 'booking_manager/search_results.html', {'rooms': rooms})
        else:
            pass
        if capacity:
            rooms = rooms.filter(room_capacity=int(capacity))
            return render(request, 'booking_manager/search_results.html', {'rooms': rooms})
        else:
            pass
        if projector_boolean:
            rooms = rooms.filter(projector_availability=True)
            return render(request, 'booking_manager/search_results.html', {'rooms': rooms})
        else:
            pass

        if not room_name and not capacity and not projector_boolean:
            return render(request, 'booking_manager/no_results.html', context={'rooms': rooms})

    return render(request, 'booking_manager/room_search.html', {'rooms': rooms})

