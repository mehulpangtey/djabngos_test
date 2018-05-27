from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import pytz
from datetime import datetime
import requests

from . import serializers
from . import models
from . import permissions

# -------------------------Check-in views-------------------------

class CheckinSessionApiView(APIView):
    """Checkin session API View."""

    serializer_class = serializers.SessionCheckSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        return Response({'API': 'Entry'})

    def post(self, request):
        """Check-in query."""

        serializer = serializers.SessionCheckSerializer(data=request.data)

        if serializer.is_valid():
            tag_id = serializer.data.get('tag_id')
            prefix_type = serializer.data.get('prefix_type')


            try:
                tag_query = models.Consumer_id.objects.get(tag_id = tag_id)
                tag_user_name = tag_query.consumer_name
                tag_user_id = tag_query.consumer_user_id
                tag_info = 'Welcome {0}'.format(tag_user_name)
                statusCode = status.HTTP_200_OK
                """Checking for tag id in consumer id table."""

                try:
                    pass_query = models.Consumer_pass.objects.get(consumer_user_id = tag_user_id)
                    pass_parking_lot_id = pass_query.parking_lot_id
                    pass_parking_id = pass_query.parking_id
                    """Checking if user is authorise to park or not, by checking pass table."""

                    if models.Parking_session.objects.filter(pass_status = 'ACTIVE',entry_consumer_identification_id = tag_id).exists():
                        """Checking for active pass, one tag one active session."""

                        tag_info = 'User vehiscle is already parked inside'
                        statusCode = status.HTTP_400_BAD_REQUEST

                    else:

                        india_timezone = pytz.timezone('Asia/Kolkata')
                        current_time = datetime.now(india_timezone)
                        """Indian timezone"""

                        """-----------get lane id from prefix_type----------"""
                        prefix_query = models.Device_Detail_Feed.objects.get(is_prefix = prefix_type)
                        entry_parking_lane_id = prefix_query.lane_id
                        entry_parking_lane_type = prefix_query.lane_type

                        checkin_session_insert = models.Parking_session(checkin_time=current_time,checkout_time='NULL',pass_status='ACTIVE',parking_lot_id=pass_parking_lot_id,consumer_user_id=tag_user_id,company_id='0',bay_id='0',entry_consumer_identification_id=tag_id,exit_consumer_identification_id='0',parking_id=pass_parking_id,special='NONE',booking_id='0',entry_lane_id=entry_parking_lane_id,exit_lane_id='0',customer_token='0',tenant='GMP',user_profile_id='1')
                        checkin_session_insert.save()
                        #
                        event_ping_log = models.Event_ping(consumer_user_id=tag_user_id,tag_id=tag_id, ping_type='CHCKIN_EVENT',lane_id=entry_parking_lane_id, event_response='SUCCESS')
                        event_ping_log.save()
                        #
                        vms_message_ping = models.VMS_message(message='Hello {0} **'.format(tag_user_name),is_dafault='0')
                        vms_message_ping.save()



                except models.Consumer_pass.DoesNotExist:
                    # request to vms with display message
                    # requests.get('http://192.168.0.26/msg=No Pass **', allow_redirects=False, stream=True).raise_for_status()
                    # end_headers()
                    tag_info = 'No pass created'
                    message = 'status : {0}'.format(tag_info)
                    statusCode = status.HTTP_400_BAD_REQUEST
                    return Response({ message}, statusCode)


            except models.Consumer_id.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            # tag_query = models.Consumer_id.objects.get(tag_id = tag_id)

            message = 'status : {0}'.format(tag_info)

            return Response({ message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------Event Trigger View-------------------------

class EventTriggerApiView(APIView):
    """Check-in and Check-out session event API View."""

    serializer_class = serializers.SessionCheckSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        return Response({'API': 'Event Trigger API'})

    def post(self, request):
        """Check-in query."""

        serializer = serializers.SessionCheckSerializer(data=request.data)
        if serializer.is_valid():
            tag_id = serializer.data.get('tag_id')
            prefix_type = serializer.data.get('prefix_type')



            if models.Device_Detail_Feed.objects.filter(is_prefix=prefix_type).exists():

                prefix_query = models.Device_Detail_Feed.objects.get(is_prefix = prefix_type)
                parking_lane_id = prefix_query.lane_id
                parking_lane_type = prefix_query.lane_type
                parking_device_type = prefix_query.device_type

                if parking_lane_type == 'ENTRY':


                    if models.Consumer_id.objects.filter(tag_id=tag_id, tag_type=parking_device_type).exists():

                        tag_query = models.Consumer_id.objects.get(tag_id=tag_id, tag_type=parking_device_type)
                        tag_user_name = tag_query.consumer_name
                        tag_user_id = tag_query.consumer_user_id
                        tag_info = 'Welcome {0}'.format(tag_user_name)
                        statusCode = status.HTTP_200_OK
                        """Checking for tag id and device type in consumer id table."""

                        try:
                            pass_query = models.Consumer_pass.objects.get(consumer_user_id = tag_user_id)
                            pass_parking_lot_id = pass_query.parking_lot_id
                            pass_parking_id = pass_query.parking_id
                            pass_lot_type = pass_query.lot_type
                            """Checking if user is authorise to park or not, by checking pass table."""

                            if models.Parking_session.objects.filter(pass_status = 'ACTIVE',consumer_user_id = tag_user_id).exists():
                                """Checking for active pass, one tag one active session."""

                                tag_info = 'Vehicle is already parked here'
                                message = 'status : {0}'.format(tag_info)
                                statusCode = status.HTTP_400_BAD_REQUEST
                                return Response({ message}, statusCode)

                            else:

                                india_timezone = pytz.timezone('Asia/Kolkata')
                                current_time = datetime.now(india_timezone)
                                """Indian timezone"""


                                checkin_session_insert = models.Parking_session(checkin_time=current_time,checkout_time='NULL',pass_status='ACTIVE',parking_lot_id=pass_parking_lot_id,consumer_user_id=tag_user_id,company_id='0',bay_id='0',entry_consumer_identification_id=tag_id,exit_consumer_identification_id='0',parking_id=pass_parking_id,lot_type=pass_lot_type,special='NONE',booking_id='0',entry_lane_id=parking_lane_id,exit_lane_id='0',customer_token='0',tenant='GMP',user_profile_id='1')
                                checkin_session_insert.save()
                                #
                                event_ping_log = models.Event_ping(consumer_user_id=tag_user_id,tag_id=tag_id, ping_type='CHCKIN_EVENT',lane_id=parking_lane_id, event_response='SUCCESS')
                                event_ping_log.save()
                                #
                                vms_message_ping = models.VMS_message(message='Hello {0} **'.format(tag_user_name),is_dafault='0')
                                vms_message_ping.save()

                                message = 'status : {0}'.format(tag_info)
                                return Response({ message}, statusCode)




                        except models.Consumer_pass.DoesNotExist:
                            # request to vms with display message
                            # requests.get('http://192.168.0.26/msg=No Pass **', allow_redirects=False, stream=True).raise_for_status()
                            # end_headers()
                            tag_info = 'No pass created'
                            message = 'status : {0}'.format(tag_info)
                            statusCode = status.HTTP_400_BAD_REQUEST
                            return Response({ message}, statusCode)


                    else:
                        statusCode = status.HTTP_400_BAD_REQUEST
                        msg = "Tag is not available!"
                        message = 'status : {0}'.format(msg)
                        return Response({ message}, statusCode)


                else:
                    if models.Consumer_id.objects.filter(tag_id=tag_id, tag_type=parking_device_type).exists():

                        india_timezone = pytz.timezone('Asia/Kolkata')
                        current_time = datetime.now(india_timezone)
                        """Indian timezone"""

                        tag_query = models.Consumer_id.objects.get(tag_id=tag_id, tag_type=parking_device_type)
                        tag_user_name = tag_query.consumer_name
                        tag_user_id = tag_query.consumer_user_id
                        """Checking for tag id and device type in consumer id table."""

                        if models.Parking_session.objects.filter(pass_status = 'ACTIVE',consumer_user_id = tag_user_id).exists():

                            models.Parking_session.objects.filter(pass_status = 'ACTIVE',consumer_user_id = tag_user_id).update(checkout_time=current_time,pass_status='COMPLETED',exit_consumer_identification_id=tag_id,exit_lane_id=parking_lane_id)
                            vms_message_ping = models.VMS_message(message='thank you **')
                            vms_message_ping.save()
                            msg = "Thank you!"
                            statusCode = status.HTTP_200_OK
                            message = 'status : {0}'.format(msg)
                            return Response({ message}, statusCode)
                        else:
                            msg = "This tag is not identified! 3"
                            statusCode = status.HTTP_400_BAD_REQUEST
                            message = 'status : {0}'.format(msg)
                            return Response({ message}, statusCode)
                            #requests.get('http://192.168.0.26/msg=Thank you **', allow_redirects=False, stream=True).raise_for_status()
                    else:
                        statusCode = status.HTTP_400_BAD_REQUEST
                        msg = "This tag is not identified! 2"
                        message = 'status : {0}'.format(msg)
                        return Response({ message}, statusCode)


            else:
                statusCode = status.HTTP_400_BAD_REQUEST
                msg = "Device is not identified! 1"
                message = 'status : {0}'.format(msg)
                return Response({ message}, statusCode)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -------------------------Check-out views-------------------------

class CheckoutSessionApiView(APIView):
    """Checkout session API View."""

    serializer_class = serializers.SessionCheckSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        return Response({'API': 'Exit'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        serializer = serializers.SessionCheckSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            exit_tag_id = serializer.data.get('tag_id')
            prefix_type = serializer.data.get('prefix_type')


            india_timezone = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(india_timezone)
            """Indian timezone"""

            try:
                tag_query = models.Consumer_id.objects.get(tag_id = exit_tag_id)
                tag_user_name = tag_query.consumer_name
                tag_user_id = tag_query.consumer_user_id

                if models.Parking_session.objects.filter(pass_status = 'ACTIVE',consumer_user_id = tag_user_id).exists():

                    """-----------get lane id from prefix_type----------"""
                    prefix_query = models.Device_Detail_Feed.objects.get(is_prefix = prefix_type)
                    exit_parking_lane_id = prefix_query.lane_id
                    exit_parking_lane_type = prefix_query.lane_type

                    models.Parking_session.objects.filter(pass_status = 'ACTIVE',consumer_user_id = tag_user_id).update(checkout_time=current_time,pass_status='COMPLETED',exit_consumer_identification_id=exit_tag_id,exit_lane_id=exit_parking_lane_id)
                    msg = "Thank you!"
                    statusCode = status.HTTP_200_OK
                else:
                    msg = "This tag is not identified!"
                    statusCode = status.HTTP_400_BAD_REQUEST
                # requests.get('http://192.168.0.26/msg=Thank you **', allow_redirects=False, stream=True).raise_for_status()
            except models.Parking_session.DoesNotExist:
                msg = "This tag is not identified!"
                statusCode = status.HTTP_400_BAD_REQUEST

            message = 'status : {0}'.format(msg)

        else:
            statusCode = status.HTTP_400_BAD_REQUEST
            msg = "This tag is not identified!"
            message = 'status : {0}'.format(msg)

        return Response({ message}, statusCode)


# -------------------------Profile views-------------------------

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, creating and updating profiles."""

    
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

# -------------------------Login views-------------------------

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)

# -------------------------Device Detail views-------------------------

class DeviceDetailFeedViewSet(viewsets.ModelViewSet):
    """Handels creating, reading and updating device detail feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.DeviceDetailFeedSerializer
    queryset = models.Device_Detail_Feed.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, )

    def perform_create(self, serializer):
        """Sets the device detail to the logges in user."""

        serializer.save(user_profile=self.request.user)

# -------------------------Corporate table views-------------------------

class CorporateDetailViewset(viewsets.ModelViewSet):
    """Handels creating, reading and updating corporate detail feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CorporateDetailFeedSerializer
    queryset = models.Corporate_Detail.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, )

    def perform_create(self, serializer):
        """Sets the corporate detail to the logges in user."""

        serializer.save()

# -------------------------Consumer views-------------------------

class ConsumerIDViewset(viewsets.ModelViewSet):
    """Handels creating, reading and updating consumer ID detail feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ConsumerIDSerializer
    queryset = models.Consumer_id.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, )

    def perform_create(self, serializer):
        """Sets the corporate detail to the loggs in user."""

        serializer.save()

# -------------------------Consumer pass views-------------------------

class ConsumerPassViewset(viewsets.ModelViewSet):
    """Handels creating, reading and updating consumer Pass detail feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ConsumerPassSerializer
    queryset = models.Consumer_pass.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('consumer_vehicle_number', 'pass_status','parking_id','pass_master_id',)

    def perform_create(self, serializer):
        """Sets the consumer pass detail to the logges in user."""

        serializer.save()

# -------------------------Parking session views-------------------------

class ParkingSessionViewset(viewsets.ModelViewSet):
    """Handels creating, reading and updating consumer Pass detail feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ParkingSessionSerializer
    queryset = models.Parking_session.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('pass_status', 'checkin_time',)
    http_method_names = ['get', 'head']


    def perform_create(self, serializer):
        """Sets the consumer pass detail to the logges in user."""

        serializer.save()

class LastCompleteActiveSession(viewsets.ModelViewSet):
    """Handels last 10 completed session feed items."""

    serializer_class = serializers.CompleteParkingSessionSerializer
    queryset = models.Parking_session.objects.filter(pass_status = 'COMPLETED').order_by('-checkin_time')[:10]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    http_method_names = ['get', 'head']

class LiveActiveSession(viewsets.ModelViewSet):
    """Handels last 10 active live session feed items."""

    serializer_class = serializers.LiveParkingSessionSerializer
    queryset = models.Parking_session.objects.filter(pass_status = 'ACTIVE').order_by('-checkin_time')[:10]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )
    http_method_names = ['get', 'head']

class DeviceDetailSession(viewsets.ModelViewSet):
    """Handels last 10 active live session feed items."""

    serializer_class = serializers.DeviceDetailFeedSerializer
    queryset = models.Device_Detail_Feed.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )