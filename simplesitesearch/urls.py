from django.urls import re_path

from . import indexing_views, views

urlpatterns = [
    re_path(r'^$', views.SearchResult.as_view(), name='search'),
    re_path(
        r'^internal/indexing/token/?$',
        indexing_views.obtain_indexing_token,
        name='sss_indexing_token',
    ),
    re_path(
        r'^internal/indexing/refresh/?$',
        indexing_views.refresh_indexing_token,
        name='sss_indexing_refresh',
    ),
]
