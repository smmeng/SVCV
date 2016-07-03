
from rest_framework import permissions
from functools import wraps
from django.http import HttpResponseRedirect
from django.conf import settings

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
    
class PublicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated()

class IsAdminOrIsSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is supersuser
        return view.action == 'retrieve' or request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details,
        # allows superuser to view all records
        return request.user.is_staff or request.user.is_superuser or obj == request.user
        #return obj.user == request.user or request.user.is_staff or request.user.is_superuser
    
    
class IsAdminOrIsSelf2(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if (request.user.is_staff or request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated()):
            return True
        return False
    
def is_superuser(f):
    @wraps(f)
    def wrapper(request, *args, **kwds):
        print "In is_superuser()"
        if request.user.is_superuser:
            return f(request, *args, **kwds)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return wrapper

def is_staff(f):
    @wraps(f)
    def wrapper(request, *args, **kwds):
        print "In is_staff)"
        if request.user.is_staff:
            return f(request, *args, **kwds)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return wrapper

def is_staffOrSelf(f):
    @wraps(f)
    def wrapper(request, *args, **kwds):
        user = request.user
        investorId = request.parameters['investorId']
        print "In is_staffOrSelf() user=", user, " investorId=", investorId
        if request.user.is_staff or user == investorId:
            return f(request, *args, **kwds)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return wrapper