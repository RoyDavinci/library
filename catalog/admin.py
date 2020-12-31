from catalog.models import Author, Book, BookInstance, Genre, Language
from django.contrib import admin
from .models import Book, BookInstance, Language, Author, Genre

# Register your models here.


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInstanceInline(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
    


admin.site.register(Book, BookAdmin)


class BookInstanceAdmin(admin.ModelAdmin):

    list_filter = ('status', 'due_back', "book", "id")
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', "borrower")
        }),
    )


admin.site.register(BookInstance, BookInstanceAdmin)


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInstanceInline]


admin.site.register(Author, AuthorAdmin)


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
