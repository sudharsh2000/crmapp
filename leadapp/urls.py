from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from leadapp.views import LeadViewSet, NoteViewSet

router = DefaultRouter()
router.register('lead', LeadViewSet, basename='leads')

leads_router = routers.NestedDefaultRouter(router, 'lead', lookup='lead')
leads_router.register('notes', NoteViewSet, basename='lead-notes')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(leads_router.urls)),
]