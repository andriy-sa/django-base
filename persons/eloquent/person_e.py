from orator import Model
from orator.orm import has_many, has_one
from .comment_e import Comment

class Person(Model):

    __table__ = 'persons_person'
    __timestamps__ = False

    @has_many('person_id')
    def comments(self):
        return Comment

    @has_one('person_id')
    def last_comment(self):
        return Comment.order_by('id','desc')