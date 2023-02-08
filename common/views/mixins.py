from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from common.serializers.mixins import DictMixinSerializer


class ExtendedGenericViewSet(GenericViewSet):
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    pass


class DictListMixin(ListViewSet):
    serializer_class = DictMixinSerializer
    pagination_class = None  # убрал пагинацию


class CRUViewSet(ExtendedGenericViewSet,  # миксин CRUD без удаления
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 ):
    pass


class CRUDViewSet(CRUViewSet,
                  mixins.DestroyModelMixin,  # миксин CRUD с удалением
                  ):
    pass
