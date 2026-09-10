from rest_framework.permissions import BasePermission

from leadapp.models import Lead


class IsLead(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
class IsNoteLeadOwner(BasePermission):
    def has_permission(self, request, view):
        lead_pk = view.kwargs.get('lead_pk')
        if lead_pk:
            try:
                lead = Lead.objects.get(pk=lead_pk)
                return lead.owner == request.user
            except Lead.DoesNotExist:
                return False
        return True
    def has_object_permission(self, request, view, obj):
        return obj.lead.owner == request.user