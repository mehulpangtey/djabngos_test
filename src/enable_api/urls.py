from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register('viewset', views.HelloViewSet, base_name='viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('device', views.DeviceDetailFeedViewSet)
router.register('corporate', views.CorporateDetailViewset)
router.register('consumer_id', views.ConsumerIDViewset)
router.register('consumer_pass', views.ConsumerPassViewset)
router.register('parking_session', views.ParkingSessionViewset)
router.register('last_complete_list', views.LastCompleteActiveSession, base_name='last_complete_list')
router.register('active_list', views.LiveActiveSession, base_name='active_list')
router.register('device_feed', views.DeviceDetailSession)

urlpatterns = [
    url(r'^checkin_event/', views.CheckinSessionApiView.as_view()),
    url(r'^checkout_event/', views.CheckoutSessionApiView.as_view()),
    url(r'^event_trigger/', views.EventTriggerApiView.as_view()),
    url(r'', include(router.urls))
]