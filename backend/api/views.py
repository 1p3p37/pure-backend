from rest_framework.generics import GenericAPIView

from base.support_functions.responses import _get_response  # noqa: I100


class HealthcheckAPIView(GenericAPIView):
    serializer_class = None

    def _healcheck(self):
        return _get_response('I\'m alive!')

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request):
        return self._healcheck()
