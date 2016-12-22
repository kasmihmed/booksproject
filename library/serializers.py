from rest_framework import serializers
from books.helpers import SlugifyUniquely
from library.models import Book,Genre
from rest_framework.fields import CurrentUserDefault

GENRE_CHOICES = Genre.objects.all().values('slug')

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=True, max_length=60)
    slug = serializers.SlugField(max_length=50, min_length=None, allow_blank=True, required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    genres = serializers.SlugRelatedField(slug_field = 'slug', many=True, read_only=True,)
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Book` instance, given the validated data.
        """
        #validated_data["author"] = self.context['request'].user
        validated_data["slug"] = SlugifyUniquely(validated_data["title"],Book)
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Genre` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.slug = SlugifyUniquely(instance.title ,Book)
        instance.save()
        return instance


class GenreSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=30)
    slug = serializers.SlugField(max_length=50, min_length=None, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Genre` instance, given the validated data.
        """
        #self.slug = SlugifyUniquely(self.title,Genre)
        validated_data['slug'] = SlugifyUniquely(validated_data['title'],Genre)
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Genre` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        #instance.code = validated_data.get('code', instance.code)
        #instance.linenos = validated_data.get('linenos', instance.linenos)
        #instance.language = validated_data.get('language', instance.language)
        #instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance