from django.db import models

# Create your models here.
from django.utils import timezone

import reprlib


class Weibo(models.Model):
    weiboID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __repr__(self):
        return "{!r}".format(self.name)

    def __str__(self):
        return self.name


class Post(models.Model):
    from_id = models.ForeignKey(Weibo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    hashtag = models.CharField(max_length=200, default='')
    text = models.TextField()

    def __repr__(self):
        return "%s" % reprlib.repr(self.text)


class Seq2SeqPost(models.Model):
    from_id = models.ForeignKey(Weibo, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    hashtag = models.CharField(max_length=200, default='')
    text = models.TextField()

    abstract = models.CharField(max_length=512)

    def __init__(self, *args, **kw):
        super(Seq2SeqPost, self).__init__(*args, **kw)
        self.body = self.text

    def __repr__(self):
        return "%s" % reprlib.repr(self.abstract)

    def __eq__(self, other):
        if not isinstance(other, Seq2SeqPost):
            return NotImplemented
        return str(self.from_id) == str(other.from_id) and \
               self.abstract == other.abstract
