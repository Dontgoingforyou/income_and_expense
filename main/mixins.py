class UserQuerySetMixin:
    """
    Миксин для фильтрации QuerySet по текущему пользователю.
    Предполагается, что используется с Django CBV, где self.request доступен.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
