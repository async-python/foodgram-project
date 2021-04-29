from django.http import Http404


class AuthorPermissionMixin:
    def has_permissions(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super(AuthorPermissionMixin, self).dispatch(
            request, *args, **kwargs)
