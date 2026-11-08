from rest_framework import permissions
from django.db.models import Q
from .models import ConnectionRequest


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission for BikeTrip:
    - Safe methods (GET, HEAD, OPTIONS) are allowed to all users.
    - Write/Delete methods (POST, PUT, PATCH, DELETE) require authentication
      and the object's owner must match request.user (or user is staff).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        # If the trip has no owner assigned, only staff can modify/delete it
        if not obj.user:
            return bool(request.user.is_staff)
        return bool(obj.user == request.user or request.user.is_staff)


class IsSessionOwnerOrAcceptedParticipant(permissions.BasePermission):
    """
    Object-level permission for TripSession:
    - Reads require authentication and are limited to the trip owner or a rider
      with an accepted connection request for the trip.
    - Writes are restricted to the trip owner (or staff).
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        trip = obj.bike_trip
        if request.user.is_staff:
            return True
        if not trip:
            return False
        if trip.user_id == request.user.id:
            return True
        if request.method in permissions.SAFE_METHODS:
            return ConnectionRequest.objects.filter(
                bike_trip_id=trip.pk,
                status=ConnectionRequest.STATUS_ACCEPTED,
            ).filter(
                Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)
            ).exists()
        return False


class IsConnectionParticipant(permissions.BasePermission):
    """
    Permission for ConnectionRequest:
    - Only authenticated users can access connection requests.
    - Users can only view, respond to, or delete connection requests where they
      are either the sender or the receiver.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(
            obj.sender == request.user or
            obj.receiver == request.user or
            request.user.is_staff
        )
