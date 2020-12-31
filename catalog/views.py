from django.shortcuts import render
from catalog.models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewalBookModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact="a").count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_authors": num_authors,
        "num_instances_available": num_instances_available,
        "num_genres": num_genres,
        "num_visits": num_visits
    }

    return render(request, "index.html", context=context)


class BookListView(ListView):
    model = Book
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    paginate_by = 10


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksByUserListView(ListView):
    model = Book
    template_name = 'catalog/borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="b")


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == "Post":
        form = RenewalBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('library'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewalBookModelForm(
            initial={'due_back': proposed_renewal_date})
    context = {
        'form': form,
        "book_instance": book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    initial = {'date_of_death': '11/06/2020'}


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


class AuthorUpdate(UpdateView):
    model = Author
    fields = "__all__"
    

class BookCreate(CreateView):
    model =  Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    initial = {'genre': 'fiction'}
    
class BookDelete(DeleteView):
    model =  Book
    success_url = reverse_lazy("books")
    
    
class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"
