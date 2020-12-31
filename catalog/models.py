from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    name = models.CharField(
        max_length=40, help_text="Enter a book Genre eg:(Science Fiction)")

    def __str__(self):
        return self.name 


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=200, help_text="Write a breif description of the book")
    isbn = models.CharField("1500", max_length=15, unique=True,
                            help_text='15 characters Character < a href="https://www.isbn-international.org/content/what-isbn" > ISBN number < /a >')
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="This provides unique identification for all books")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', "Maintenance"),
        ("o", "On Loan"),
        ("a", "Available"),
        ("r", "reserved"),
        ("b", "borrowed")
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book Availability"
    )

    class Meta():
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"({self.book.title}) ({self.status}) ({self.due_back}) {self.id}"

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField("Dead", blank=True, null=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return  f"{self.first_name} {self.last_name}"


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
