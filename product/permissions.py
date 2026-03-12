from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):

        # пользователь должен быть авторизован
        if not request.user.is_authenticated:
            return False

        # должен быть staff
        if not request.user.is_staff:
            return False

        # запрет на создание продуктов
        if request.method == "POST":
            return False

        return True




