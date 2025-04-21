from rest_framework.generics import ListAPIView, RetrieveAPIView

from movies.api.v1.pagination import FilmWorkPagination
from movies.api.v1.serializers import FilmWorkSerializer
from movies.models import FilmWork


class FilmWorkListView(ListAPIView):
    """Получение списка всех кинопроизведений."""
    queryset = FilmWork.objects.prefetch_related(
        'genres', 'persons', 'personfilmwork_set'
    ).all()
    serializer_class = FilmWorkSerializer
    pagination_class = FilmWorkPagination
    http_method_names = ('get',)


class FilmWorkDetailView(RetrieveAPIView):
    """Получение детальной информации о конкретном кинопроизведении."""
    queryset = FilmWork.objects.prefetch_related('genres', 'persons')
    serializer_class = FilmWorkSerializer
    http_method_names = ('get',)
