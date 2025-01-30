from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   #gives status codes WITH A HANDY RESPONSE
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from api import serializers
from api import models
from api import permissions

class HelloApiView(APIView):
    """Test API View"""
    serializer_class= serializers.HelloSerializer

    # to retrieve an object or list of objects
    def get(self, request, format=None):
            """Returns a list of APIView features"""
            an_apiview=[
             'Users HTTP methods as function (get, post, patch, put, delete)',
             'Is similar to traditional Django View',
             'Gives you most control over your application logic',
             'Is mapped manually to URLs',
            ]

            return Response({'message':'Hello!', 'an_apiview':an_apiview})

    def post(self, request):
            """Create a hello message with our name"""
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                    name = serializer.validated_data.get('name')
                    message=f'Hello {name}'
                    return Response({'message':message})
            else:
                return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                    )

#to update an object
    def put(self, request, pk=None):
        """Handle updating object"""
        return Response ({'method': 'PUT'})

#to partially update an object
    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        return Response ({'method': 'PATCH'})


#to delete
    def delete(self, request, pk=None):
        """Delete an object"""
        return Response ({'method': 'DELETE'})


# Viewset in parameter is the basic viewset class that drf provides
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class= serializers.HelloSerializer


    def list(self, request):
            """Return a hello message"""
            a_viewset=[
                'Uses actions (list, create, retrieve, update, partial_update)',
                'Automatically maps to URLs using roters',
                'Provides more functionality with less code',

            ]
            return Response({'message':'Hello', 'a_viewset':a_viewset})

    def create(self, request):
            """Create a new hello message"""
            serializer=self.serializer_class(data=request.data)

            if serializer.is_valid():
                name= serializer.validated_data.get('name')
                message= f'Hello{name}!'
                return Response({'message':message})
            else:
                return Response(
                   serializer.errors,
                   status = status.HTTP_400_BAD_REQUEST
                )

#retrieve a specifc object in our viewsets witha specific primary key id passed
    def retrieve(self, request, pk=None):
            """Handle getting an object by its ID"""
            return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handle updating of an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle partial updating of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
            """Handle deleting of an object"""
            return Response({'http_method':'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class= serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()

    #how user will authenticate
    #add a coma so python knows it is a tuple
    authentication_classes=(TokenAuthentication, )

    #how permissions will be granted to user to do certain things
    #add a coma so python knows it is a tuple
    permission_classes=(permissions.UpdateOwnProfile,)
    #filter_backends is defined in DRF's GenericAPIView,
    #which is the base class for most DRF views
    #like ModelViewSet and APIView
    filter_backends = (filters.SearchFilter,)

    #if we search a specific letter it will return all fields having that letter
    search_fields=('name', 'email',)
    print( 'email')


#base class ObtainAuthToken to handle token-based authentication
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating feed items"""
    authentication_classes= (TokenAuthentication, )
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes = (
      permissions.UpdateOwnStatus,
      # IsAuthenticatedOrReadOnly if you want to allow unauthenticated users to see the feed as well

      #only authenticated users can see feed
      IsAuthenticated,
    )
    # to estrict to see only their own feed
    # def get_queryset(self):
    #     return self.queryset.filter(user_profile=self.request.user)

    def perform_create(self, serializer):
        """Sets user profile to logged in user"""
        #user field is added whenever the user is authenticated else it is set to an anonymous user account
        serializer.save(user_profile=self.request.user)
