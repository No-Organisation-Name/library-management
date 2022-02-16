from django.db import models


class Contributor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contributor'


class Category(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Book(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='books', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    publisher = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    publication_year = models.CharField(max_length=5)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    date_of_entry = models.DateField()
    image = models.ImageField(upload_to='books/', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'book'
