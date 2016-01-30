from myapp.utility import Utility
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import   User

################## To generate all user list based on the current role
@login_required
def adminGetAllUsers(request):
    user = request.user
    print 'get_activity() ] user=[', user

    if user.is_staff or user.is_superuser:
        util = Utility()
        user_list = util.viewable_user_list(request)
    
    #allUserId_list = user_list['allUserId_list']
    #allUser_list = user_list['allUser_list']

    
    #activity_dict= {'allUserId_list', 'allUser_list':allUser_list, 'investorId':uid, 'investorName':userName}
    #print 'get_activity() activity_dict[', activity_dict
    # We also add the project object from the database to the context dictionary.
    # We'll use this in the template to verify that the project exists.
    #activity_dict['projects'] = activity_list

    # Go render the response and return it to the client.
    return user_list


from django.http import Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response

from myapp.models import InvestmentActivity
from myapp.serializers import InvestorSerializer, ProjectSerializer, UserSerializer

class InvestorList(APIView):
    """
    List all investor details, or create a new snippet.
    """
    def get(self, request, Pid, format=None):
        print ' Get Pid=[', Pid
        investors = InvestmentActivity.objects.filter(ProjectId=Pid)
        serializer = InvestorSerializer(investors, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class InvestorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    print ' InvestorViewSet=[', 
    serializer_class = InvestorSerializer
    
    queryset = InvestmentActivity.objects.all()
    #print queryset
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('ProjectId', 'UserId', 'Type')
    
    ##permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    
