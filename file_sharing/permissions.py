from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # проверка является ли метод безопасным (GET, HEAD, OPTIONS)
            return True
        return obj.user == request.user # сравнение пользователя этого обьекта и пользователя по сесcии