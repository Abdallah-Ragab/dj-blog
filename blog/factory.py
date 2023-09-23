from factory.django import DjangoModelFactory
from factory.faker import faker
from factory import Iterator, LazyAttribute, Faker as FakerFactory
from .models import Post
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = FakerFactory('sentence', nb_words=4)
    body = FakerFactory('paragraph', nb_sentences=20, variable_nb_sentences=True)
    status =FakerFactory('random_element', elements=Post.Status.values)
    author = Iterator(get_user_model().objects.all())

