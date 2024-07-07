from django.db import models

# Create your models here.


class Room(models.Model):
    room_name = models.CharField(max_length=255)
    room_capacity = models.IntegerField()
    projector_availability = models.BooleanField(True)


class RoomReservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('date', 'room_id')
