from rest_framework import viewsets, throttling, filters
from django_filters.rest_framework import DjangoFilterBackend


from .models import Achievement, Cat, User
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    # throttle_classes = (WorkingHoursRateThrottle , throttling.AnonRateThrottle,)
    # throttle_scope = 'low_request'
    # Даже если на уровне проекта установлен PageNumberPagination
    # Для котиков будет работать LimitOffsetPagination
    # pagination_class = pagination.LimitOffsetPagination

    # Вот он наш собственный класс пагинации с page_size=20
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields  = ('color', 'birth_year')
    search_fields  = ('^name', 'achievements__name')
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     queryset = Cat.objects.all()
    #     color = self.request.query_parms.get('color')
    #     # Через ORM отфильтровать объекты модели Cat
    #     # по значению параметра color, полученного в запросе
    #     if color is not None:
    #         queryset = queryset.filter(color=color)
    #         return queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
