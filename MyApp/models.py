from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', default = 'media/photos/userphoto-defaultphoto.png')
    bio = models.TextField()
    phone = models.CharField(max_length=10 , blank=True , null=True)
    mail = models.EmailField()
    BaridiMob = models.CharField(max_length=100 , blank=True , null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2 , default=0 , blank=True , null=True )

    def __str__(self):
        return self.user.username


class Product(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    desc = models.TextField()
    CATEGORY_CHOICES = [
        ('Contenus Numériques', 'Contenus Numériques'),
        ('Logiciels & Applications', 'Logiciels & Applications'),
        ('Formations & Éducation en Ligne','Formations & Éducation en Ligne'),
        ('Création & Média', 'Création & Média'),
        ('Outils pour Créateurs & Entrepreneurs', 'Outils pour Créateurs & Entrepreneurs'),
        ('Divertissement & Gaming','Divertissement & Gaming'),
        ('Services Professionnels Digitalisés','Services Professionnels Digitalisés'),
        ('Communautés en Ligne','Communautés en Ligne'),
        ('Produits Tech Avancés','Produits Tech Avancés'),
        ('Investissement & Finance Digitale','Investissement & Finance Digitale'),
        ('Autres types','Autres types')
    ]
    category = models.CharField(
        max_length=200,
        choices=CATEGORY_CHOICES,
        default='Contenus Numériques'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    file = models.FileField(upload_to='products/')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name 

class Images(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    buyer = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)

    total_amount= models.DecimalField(max_digits=10,decimal_places=2)
    commission = models.DecimalField(max_digits=10,decimal_places=2)
    seller_amount = models.DecimalField(max_digits=10,decimal_places=2)

    chargily_id = models.CharField(max_length=200, null=True , blank=True)
    status = models.CharField(
        max_length=100,
        choices=[('PAN', 'Pending'), ('PAID', 'Paid')],
        default='PAN'   # يجب أن يطابق الخيار الصحيح
)
    created_at = models.DateTimeField(auto_now_add=True)