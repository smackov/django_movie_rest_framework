from rest_framework import serializers

from .models import Movie, Review
    

class FilterReviewListSerializer(serializers.ListSerializer):
    """The filter of reviews. Only parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
        
        
class RecursiveSerializer(serializers.Serializer):
    """Output children recursively"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
        

class ReviewCreateSerializer(serializers.ModelSerializer):
    "Create new review"
    class Meta:
        model = Review
        fields = "__all__"
        

class ReviewSerializer(serializers.ModelSerializer):
    "Show the review"
    children = RecursiveSerializer(many=True)
    
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')
    

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
