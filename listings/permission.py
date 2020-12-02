from rest_framework.permissions import BasePermission


class AgentOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_agent


class UserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class OwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.agent.user_id
