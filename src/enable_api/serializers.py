from rest_framework import serializers
from . import models


class SessionCheckSerializer(serializers.Serializer):
        """serializer a name field for parking session APIView."""

        tag_id = serializers.IntegerField(default=0)
        prefix_type = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class DeviceDetailFeedSerializer(serializers.ModelSerializer):
    """A serializer for device feed items."""

    class Meta:
        model = models.Device_Detail_Feed
        fields = ('id','user_profile','created_on','lane_id','lane_type','parking_name','parking_id','company_id','hardware_master_id','device_type','device_access_address','tenant')
        extra_kwargs = {'device_detail': {'read_only': True}}

class CorporateDetailFeedSerializer(serializers.ModelSerializer):
    """A serializer for corporate detail items."""

    class Meta:
        model = models.Corporate_Detail
        fields = ('id','corporate_name','corporate_contact_number','corporate_email','corporate_address','created_on')
        extra_kwargs = {'corporate_detail': {'read_only': True}}

class ConsumerIDSerializer(serializers.ModelSerializer):
    """A serializer for consumer id detail items."""

    class Meta:
        model = models.Consumer_id
        fields = ('id','consumer_user_id','consumer_name','tag_id')
        extra_kwargs = {'consumer_user_id': {'read_only': True}}


class ConsumerPassSerializer(serializers.ModelSerializer):
    """A serializer for consumer pass detail items."""

    class Meta:
        model = models.Consumer_pass
        fields = ('id','consumer_user_id','pass_master_id','corporate_id','parking_id','parking_lot_id','consumer_vehicle_number','pass_status','is_default','payment_status','created_at','expire_at')
        extra_kwargs = {'consumer_user_id': {'read_only': True}}

class ParkingSessionSerializer(serializers.ModelSerializer):
    """A serializer for consumer pass detail items."""

    class Meta:
        model = models.Parking_session
        fields = ('id','checkin_time','checkout_time','pass_status','parking_lot_id','consumer_user_id','company_id','bay_id','entry_consumer_identification_id','exit_consumer_identification_id','parking_id','lot_type','special','booking_id','entry_lane_id','exit_lane_id','customer_token','tenant','create_at','updated_at')
        extra_kwargs = {'consumer_user_id': {'read_only': True}}

class CompleteParkingSessionSerializer(serializers.ModelSerializer):
    """A serializer for consumer pass detail items."""

    class Meta:
        model = models.Parking_session
        fields = ('id','checkin_time','checkout_time','pass_status','parking_lot_id','consumer_user_id','company_id','bay_id','entry_consumer_identification_id','exit_consumer_identification_id','parking_id','lot_type','special','booking_id','entry_lane_id','exit_lane_id','customer_token','tenant','create_at','updated_at')
        extra_kwargs = {'consumer_user_id': {'read_only': True}}

class LiveParkingSessionSerializer(serializers.ModelSerializer):
    """A serializer for consumer pass detail items."""

    class Meta:
        model = models.Parking_session
        fields = ('id','checkin_time','checkout_time','pass_status','parking_lot_id','consumer_user_id','company_id','bay_id','entry_consumer_identification_id','exit_consumer_identification_id','parking_id','lot_type','special','booking_id','entry_lane_id','exit_lane_id','customer_token','tenant','create_at','updated_at')
        extra_kwargs = {'consumer_user_id': {'read_only': True}}