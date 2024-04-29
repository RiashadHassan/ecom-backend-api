from django.core.exceptions import PermissionDenied


class CustomGetObjectOr404:
    @classmethod
    def get_object_or_404(cls, klass, *args, **kwargs):
        manager = (
            klass._default_manager
            if hasattr(klass, "_default_manager")
            else klass.objects
        )
        queryset = manager.get_queryset()
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise PermissionDenied("Permission Denied")
