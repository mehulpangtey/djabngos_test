from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helper Django work our custom user model."""

    def create_user(self, email, name, password=None):
        """Creates a new user with the given detials."""

        # Check that the user provided an email.
        if not email:
            raise ValueError('Users must have an email address.')

        # Create a new user object.
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        # Set the users password. We use this to create a password
        # hash instead of storing it in clear text.
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given detials."""

        # Create a new user with the function we created above.
        user = self.create_user(
            email,
            name,
            password
        )

        # Make this user an admin.
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Respents a "user profile" inside our system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a user full name."""

        return self.name

    def get_short_name(self):
        """Used to get a users short name."""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object to string."""

        return self.email


class Device_Detail_Feed(models.Model):
    """Device detial update."""

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    lane_id = models.IntegerField(default=0)
    lane_type = models.CharField(max_length=255)
    parking_name = models.CharField(max_length=255, default='')
    parking_id = models.IntegerField(default=0)
    company_id = models.IntegerField(default=0)
    hardware_master_id = models.IntegerField(default=0)
    device_type = models.CharField(max_length=255, default='')
    device_access_address = models.CharField(max_length=255, default='')
    tenant = models.CharField(max_length=255, default='')
    is_prefix = models.CharField(max_length=255, default='0')

    def __str__(self):
        """Return model as string."""

        return self.parking_name

class Corporate_Detail(models.Model):
    """Corporate operator detail table."""

    corporate_id = models.IntegerField(default=0)
    corporate_name = models.CharField(max_length=255, default='')
    corporate_contact_number = models.IntegerField(default=0)
    corporate_email = models.EmailField(max_length=255, unique=True)
    corporate_address = models.CharField(max_length=255, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        """Return model as string."""

        return self.corporate_name

class Consumer_id(models.Model):
    """Consumer id relation table."""

    consumer_user_id = models.IntegerField(default=0)
    consumer_name = models.CharField(max_length=255, default='')
    tag_id = models.IntegerField(default=0)
    tag_type = models.CharField(max_length=255, default='NULL')

    def __str__(self):
        """Return model as string."""

        return self.consumer_name

class Consumer_pass(models.Model):
    """Consumer pass detail table"""

    consumer_user_id = models.IntegerField(default=0)
    pass_master_id = models.IntegerField(default=0)
    corporate_id = models.IntegerField(default=0)
    parking_id = models.IntegerField(default=0)
    parking_lot_id = models.IntegerField(default=0)
    consumer_vehicle_number = models.CharField(max_length=255, default='')
    pass_status = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(auto_now_add=True)
    is_default = models.CharField(max_length=255, default='')
    payment_status = models.CharField(max_length=255, default='')
    lot_type = models.CharField(max_length=255, default='')
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        """Return model as string."""

        return self.consumer_vehicle_number

class Event_ping(models.Model):
    """Event ping table"""

    consumer_user_id = models.IntegerField(default=0)
    tag_id = models.IntegerField(default=0)
    ping_type = models.CharField(max_length=255, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    lane_id = models.IntegerField(default=0)
    event_response = models.CharField(max_length=255, default='')

    def __str__(self):
        """Return model as string."""

        return self.consumer_user_id

class Parking_session(models.Model):
    """parking check-in & check-out session table."""

    checkin_time = models.CharField(max_length=255, default='')
    checkout_time = models.CharField(max_length=255, default='')
    pass_status = models.CharField(max_length=255, default='')
    parking_lot_id = models.IntegerField(default=0)
    consumer_user_id = models.IntegerField(default=0)
    company_id = models.IntegerField(default=0)
    bay_id = models.IntegerField(default=0)
    entry_consumer_identification_id = models.CharField(max_length=255, default='')
    exit_consumer_identification_id = models.CharField(max_length=255, default='')
    parking_id = models.IntegerField(default=0)
    lot_type = models.CharField(max_length=255, default='')
    special = models.CharField(max_length=255, default='')
    booking_id = models.IntegerField(default=0)
    entry_lane_id = models.IntegerField(default=0)
    exit_lane_id = models.IntegerField(default=0)
    customer_token = models.IntegerField(default=0)
    tenant = models.CharField(max_length=255, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        """Return model as string."""

        return self.consumer_user_id

class Pass_access_slot(models.Model):
    """"Slot base pass access detail"""

    access_type = models.CharField(max_length=255, default='')
    start_minute_of_the_day = models.CharField(max_length=255, default='')
    end_minute_of_the_day = models.CharField(max_length=255, default='')
    duration = models.IntegerField(default=0)
    pass_master_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    start_day = models.IntegerField(default=0)
    end_day = models.IntegerField(default=0)
    tenant = models.CharField(max_length=255, default='')

    def __str__(self):
        """Return model as string."""

        return self.access_type

class VMS_message(models.Model):
    """VMS meesage table."""

    message = models.CharField(max_length=255, default='')
    is_dafault = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model as string."""

        return self.message