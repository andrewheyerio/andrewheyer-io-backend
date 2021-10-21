from django.core.management import BaseCommand
import re
import csv

from core.models import Movie, Actor


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('movie_plots.csv', encoding='utf-8') as f:
            i = 0
            reader = csv.reader(f)
            for i, row in enumerate(reader):

                if i == 0:
                    continue

                if i > 1000:
                    break

                release_year = row[0]
                title = row[1]
                origin_ethnicity = row[2]
                director = row[3]
                cast = re.split(':|&|;|,| and |\n', row[4])
                genre = row[5]
                wiki_page = row[6]
                plot = row[7]

                for actor in cast:
                    print("actor " + str(actor.strip()))

                    actor_obj, created = Actor.objects.get_or_create(name=actor.strip())
                    movie_obj, created = Movie.objects.get_or_create(
                        release_year=release_year,
                        title=title,
                        origin_ethnicity=origin_ethnicity,
                        director=director,
                        genre=genre,
                        wiki_page=wiki_page,
                        plot=plot
                    )

                    movie_obj.actors.add(actor_obj)
