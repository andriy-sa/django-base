from django.core.management.base import BaseCommand
from  persons.models import Person,Comment

class Command(BaseCommand):
    help = 'DB Seeder'

    persons = [
        {
            'id' : 1,
            'first_name' : 'Andriy',
            'last_name'  : 'Smolyar',
            'phone'      : '0689874569',
            'address'    : 'Rivne city'
        },
        {
            'id': 2,
            'first_name': 'Dima',
            'last_name': 'Bimba',
            'phone': '05078965423',
            'address': 'Kiev city'
        },
        {
            'id': 3,
            'first_name': 'Oleh',
            'last_name': 'Kovalchuk',
            'phone': '0569874521',
            'address': 'Odesa city'
        },
        {
            'id': 4,
            'first_name': 'Sasha',
            'last_name': 'Zifirka',
            'phone': '05896874521',
            'address': 'Lviv city'
        },
        {
            'id': 5,
            'first_name': 'Tamara',
            'last_name': 'Wooman',
            'phone': '0506547895',
            'address': 'Lutsk city'
        },
    ]

    comments = [
        {
            'id' : 1,
            'message' : 'test messge 1',
            'rate' : 4,
            'person' : 3
        },
        {
            'id': 2,
            'message': 'test messge 2',
            'rate': 1,
            'person': 5
        },
        {
            'id': 3,
            'message': 'test messge 3',
            'rate': 5,
            'person': 5
        }
    ]

    def handle(self, *args, **options):

        # seed persons if table empty
        persons_count = Person.objects.count()
        if persons_count == 0:
            for person in self.persons:
                Person.objects.create(
                    id=person['id'],
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    phone=person['phone'],
                    address=person['address']
                )

        #seed comments if table empry
        comments_count = Comment.objects.count()
        if comments_count == 0:
            for comment in self.comments:
                person = Person.objects.filter(id=comment['person']).first()
                if person:
                    Comment.objects.create(
                        id=comment['id'],
                        message=comment['message'],
                        rate=comment['rate'],
                        person=person
                    )


        self.stdout.write(self.style.SUCCESS('Successfull seeder'))
