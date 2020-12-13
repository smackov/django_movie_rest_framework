from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieViewSet.as_view({'get': 'list'})),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'})),
    path('review/', views.ReviewViewSet.as_view({'post': 'create'})),
    path('rating/', views.RatingViewSet.as_view({'post': 'create'})),
])


urlpatterns += [
    # path('movie/', views.MovieListView.as_view()),
    # path('movie/<int:pk>/', views.MovieDetailView.as_view()),
    # path('review/', views.ReviewCreateView.as_view()),
    # path('rating/', views.RatingCreateView.as_view()),
    path('actors/', views.ActorListView.as_view()),
    path('actor/<int:pk>/', views.ActorDetailView.as_view()),
]
