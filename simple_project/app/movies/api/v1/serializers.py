from movies.models import FilmWork
from rest_framework import serializers


class FilmWorkSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = FilmWork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        )

    def get_rating(self, obj):
        return obj.rating if obj.rating is not None else 0.0

    def get_genres(self, obj):
        return list({genre.name for genre in obj.genres.all()})

    def get_persons_by_role(self, obj, role):
        return list({
            pfw.person.full_name
            for pfw in obj.personfilmwork_set.all()
            if pfw.role == role
        })

    def get_actors(self, obj):
        return self.get_persons_by_role(obj, 'actor')

    def get_directors(self, obj):
        return self.get_persons_by_role(obj, 'director')

    def get_writers(self, obj):
        return self.get_persons_by_role(obj, 'writer')
