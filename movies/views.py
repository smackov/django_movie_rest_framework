from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
                          RatingCreateSerializer)


class MovieListView(APIView):
    """
    Get the list of the movies.
    """
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        serializer = RatingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
        
