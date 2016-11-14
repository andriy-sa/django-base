from orator import Model
class Comment(Model):

    __table__ = 'persons_comment'
    __timestamps__ = False