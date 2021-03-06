from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() #Менеджер по умолчанию
    published = PublishedManager() #Наш новый менеджер

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    #ForeignKey один ко многим одна статья может иметь множество коментариев
    #related_name позволяет получить доступ к коментам конкретной статьи
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)#created для сортировки коментариев в хронологическом порядке
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) #active что бы скрыть спам коментарии

    class Meta:
        ordering = ('created',)

    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}  '




