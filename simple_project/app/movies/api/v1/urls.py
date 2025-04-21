from django.urls import include, path

from movies.api.v1.views import FilmWorkDetailView, FilmWorkListView


urlpatterns = [
    path('movies/', FilmWorkListView.as_view(), name='filmwork_list'),
    path(
        'movies/<uuid:pk>/',
        FilmWorkDetailView.as_view(),
        name='filmwork_detail'
    ),
]
