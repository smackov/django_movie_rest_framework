from rest_framework import serializers

from .models import Movie, Review
        

class ReviewCreateSerializer(serializers.ModelSerializer):
    "Create new review"
    class Meta:
        model = Review
        fields = "__all__"
        

class ReviewSerializer(serializers.ModelSerializer):
    "Show the review"
    class Meta:
        model = Review
        fields = ('name', 'text', 'parent')


class MovieListSerializer(serializers.ModelSerializer):
    "List of the movies"
    class Meta:
        model = Movie
        fields = ('title', 'tagline',)       
        
        
class MovieDetailSerializer(serializers.ModelSerializer):
    "The movie"
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    
    class Meta:
        model = Movie
        exclude = ('draft',)
