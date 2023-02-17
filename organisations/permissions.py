from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsMyOrganisation(IsAuthenticated): # имеем ли мы доступ к изменению организации или нет
    def has_object_permission(self, request, view, obj):
        if obj.director == request.user:
            return True
        if request.method in SAFE_METHODS:
            return obj.employees.all(user=request.user).exists()
        return False


class IsColleagues(IsAuthenticated):  # имеем ли мы доступ к изменению сотрудника или нет
    def has_object_permission(self, request, view, obj):
        if obj.organisation.director == request.user:
            return True
        if request.method in SAFE_METHODS:
            return obj.organisation.employees.all(user=request.user).exists() # является ли пользователь сотрудником организации
        return False


class IsMyGroup(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organisation.director == request.user:
            return True
        if request.method in SAFE_METHODS:
            return obj.organisation.employees.all(
                user=request.user).exists()  # является ли пользователь сотрудником организации
        return False


class IsOfferManager(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.organisation.director == request.user:
            return True
        return False
