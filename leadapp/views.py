"""
Views and ViewSets for Lead Management System
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Lead, LeadNote
from .permissions import IsLead, IsNoteLeadOwner
from .serializers import LeadSerializer, NoteSerializer







class LeadPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_size_query_description = 'Number of results to return per page'


class LeadViewSet(viewsets.ModelViewSet):


    serializer_class = LeadSerializer
    permission_classes = [IsLead,IsAuthenticated]
    pagination_class = LeadPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'company']
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['-created_at', '-id']

    def get_queryset(self):
        return Lead.objects.filter(owner=self.request.user).prefetch_related('notes')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Lead deleted successfully. Associated notes have been removed.'}, status=status.HTTP_204_NO_CONTENT)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsNoteLeadOwner,IsAuthenticated]

    def get_queryset(self):
        lead_pk = self.kwargs.get('lead_pk')
        return LeadNote.objects.filter(lead__pk=lead_pk,lead__owner=self.request.user).order_by('created_at')



    def perform_create(self, serializer):
        lead_pk = self.kwargs.get('lead_pk')
        try:
            lead = Lead.objects.get(pk=lead_pk, owner=self.request.user)
        except Lead.DoesNotExist:
            raise NotFound('Lead not found or you do not have permission to add notes to it.')
        serializer.save(lead=lead, created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Note deleted successfully.'},status=status.HTTP_204_NO_CONTENT)