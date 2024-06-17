import csv
import os
from django.core.management.base import BaseCommand
from PlanT.PlanT_Backend.models import Place, Tag

class Command(BaseCommand):
    help = 'Load data from CSV file into the Place model'

    def handle(self, *args, **kwargs):
        # 현재 파일의 디렉토리 경로를 기준으로 csv 파일 경로를 만듭니다.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'locations_banned.csv')
        
        with open(csv_file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                index, place_id, place_name, place_type, place_longitude, place_latitude, place_tag_ids, place_time = row
                
                place = Place.objects.create(
                    place_id=int(place_id),
                    place_name=place_name,
                    place_type=int(place_type),
                    place_time=int(place_time),
                    place_latitude=float(place_latitude),
                    place_longitude=float(place_longitude)
                )

                # 쉼표로 구분된 태그 ID 문자열을 처리하여 여러 Tag 객체를 생성하거나 가져옵니다.
                tag_ids = place_tag_ids.strip("[]").split(',')
                # tag_ids = place_tag_ids.split(',')
                for tag_id in list(tag_ids):
                    tag, created = Tag.objects.get_or_create(tag_id=int(tag_id))
                    place.place_tags.add(tag)
                
            self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file_path))
