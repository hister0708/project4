from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return 0

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'

class Rating(models.Model):
    post = models.ForeignKey(Post, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)  # 1부터 5까지의 값을 저장할 수 있도록 필드 추가

    def __str__(self):
        return f'{self.post.title} - {self.rating}'
