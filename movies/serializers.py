from rest_framework import serializers

from .models import Movie, Review, Rating, Actor
    

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
    
    
class ActorListSerializer(serializers.ModelSerializer):
    "List of the actors"
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')
    
    
class ActorDetailSerializer(serializers.ModelSerializer):
    "The actor"
    class Meta:
        model = Actor
        fields = '__all__'
    

class MovieListSerializer(serializers.ModelSerializer):
    "List of the movies"
    rating_user = serializers.BooleanField()
    average_star = serializers.IntegerField()
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'average_star')       
        
        
class MovieDetailSerializer(serializers.ModelSerializer):
    "The movie"
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    
    class Meta:
        model = Movie
        exclude = ('draft',)
        
        
class RatingCreateSerializer(serializers.ModelSerializer):
    "Create or update the rating of the movie"
    class Meta:
         model = Rating
         fields = ['star', 'movie']
         
    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip = validated_data.get('ip', None),
            movie = validated_data.get('movie', None),
            defaults = {'star': validated_data.get('star')},
        )
        return rating
        