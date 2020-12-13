from django.db import models
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          RatingCreateSerializer, ActorListSerializer, ActorDetailSerializer)
from .services import get_client_ip, MovieFilter


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get the list of the movies.
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(ratings__ip=get_client_ip(self.request), then=True),
                default=False,
                output_field=models.BooleanField()
            )
        ).annotate(
            average_star=models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
        )
        return movies
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
    
# class MovieListView(generics.ListAPIView):
#     """
#     Get the list of the movies.
#     """
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = (permissions.IsAuthenticated,)
    
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Case(
#                 models.When(ratings__ip=get_client_ip(self.request), then=True),
#                 default=False,
#                 output_field=models.BooleanField()
#             )
#         ).annotate(
#             average_star=models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
#         )
#         return movies
    
    # APIView
# class MovieListView(APIView):
    # def get(self, request):
    #     movies = Movie.objects.filter(draft=False).annotate(
    #         rating_user=models.Case(
    #             models.When(ratings__ip=get_client_ip(request), then=True),
    #             default=False,
    #             output_field=models.BooleanField()
    #         )
    #     ).annotate(
    #         average_star=models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
    #     )
    #     serializer = MovieListSerializer(movies, many=True)
    #     return Response(serializer.data)
    
    
# class MovieDetailView(generics.RetrieveAPIView):
#     """
#     The detail movie view.
#     """
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer    
    
# class MovieDetailView(generics.RetrieveAPIView):
#     """
#     The detail movie view.
#     """
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
    
    # APIView
    # def get(self, request, pk):
    #     movie = Movie.objects.get(id=pk, draft=False)
    #     serializer = MovieDetailSerializer(movie)
    #     return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Create new review of a film
    """
    serializer_class = ReviewCreateSerializer
    
# class ReviewCreateView(generics.CreateAPIView):
#     """
#     Create new review of a film
#     """
#     serializer_class = ReviewCreateSerializer

    # APIView
    # def post(self, request):
    #     review = ReviewCreateSerializer(data=request.data)
    #     if review.is_valid():
    #         review.save()
    #     return Response(status=201)
    
    
class RatingViewSet(viewsets.ModelViewSet):
    """
    Create or update the rating of the movie
    """    
    serializer_class = RatingCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
        
        
    # APIView
    # def post(self, request):
    #     serializer = RatingCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(ip=get_client_ip(request))
    #         return Response(status=201)
    #     else:
    #         return Response(status=400)
        
        
class ActorListView(generics.ListAPIView):
    """
    Show the list of the actors
    """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """
    Show the actor's detail
    """
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
