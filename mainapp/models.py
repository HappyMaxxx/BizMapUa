from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Region(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    koatuu = models.CharField(max_length=100)
    img = models.ImageField(upload_to='regions/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_img_url(self):
        if self.img:
            return f'/media/regions/{self.img.name.split("/")[-1]}'
        

class Businesse(models.Model):
    CATEGORY_CHOICES = [
        ('retail', 'Роздрібна торгівля'),
        ('hospitality', 'Гостинність'),
        ('technology', 'Технології'),
        ('finance', 'Фінанси'),
        ('healthcare', 'Охорона здоров’я'),
        ('manufacturing', 'Виробництво'),
        ('construction', 'Будівництво'),
        ('education', 'Освіта'),
        ('transportation', 'Транспорт'),
        ('real_estate', 'Нерухомість'),
        ('food_and_beverage', 'Харчування та напої'),
        ('professional_services', 'Професійні послуги'),
        ('entertainment', 'Розваги'),
        ('agriculture', 'Сільське господарство'),
        ('non_profit', 'Некомерційна організація'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    site_page = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=21, choices=CATEGORY_CHOICES, default='pending')
    tags = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),
                                                      ('added', 'Added')], default='pending')
    time_create = models.DateTimeField(auto_now_add=True)

    average_rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.user.username} ({self.status})'
    
    def update_average_rating(self):
        evaluations = self.evaluation_set.all()
        if evaluations.exists():
            avg = evaluations.aggregate(models.Avg('rating'))['rating__avg']
            self.average_rating = round(avg, 1) 
            self.rating_count = evaluations.count()
        else:
            self.average_rating = 0.0
            self.rating_count = 0
        self.save()


class BuisnessePhoto(models.Model):
    businesse = models.ForeignKey(Businesse, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=f'buisnes/', blank=True, null=True)

    def get_img_url(self):
        if self.img:
            return f'/media/buisnes/{self.img.name.split("/")[-1]}'


class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Оцінка не може бути меншою за 1"),
            MaxValueValidator(5, message="Оцінка не може бути більшою за 5")
        ]
    )
    business = models.ForeignKey(Businesse, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'business']