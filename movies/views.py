from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          RatingCreateSerializer, ActorListSerializer, ActorDetailSerializer)
from .services import get_client_ip


class MovieListView(APIView):
    """
    Get the list of the movies.
    """
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(ratings__ip=get_client_ip(request), then=True),
                default=False,
                output_field=models.BooleanField()
            )
        ).annotate(
            average_star=models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
    
    
class MovieDetailView(APIView):
    """
    The detail movie view.
    """
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """
    Create new review of a film
    """
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
    
    
class RatingCreateView(APIView):
    """
    Create or update the rating of the movie
    """    
    def post(self, request):
        serializer = RatingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
        
        
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
