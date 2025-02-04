from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .forms import QuoteForm
from .models import Quote, Author


def main(request, page=1):
    quotes = Quote.objects.prefetch_related('tags').all()
    paginator = Paginator(quotes, per_page=10)

    try:
        quotes_on_page = paginator.page(page)
    except EmptyPage:
        quotes_on_page = paginator.page(paginator.num_pages)

    return render(request, 'quotes/index.html', {'quotes': quotes_on_page})


def author_bio(request, fullname):
    author = get_object_or_404(Author, fullname=fullname)
    return render(request, 'quotes/author.html', {'author': author})


@login_required
def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('quotes:root')
    else:
        form = QuoteForm()

    return render(request, 'quotes/new_quote.html', {'form': form})




@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, user=request.user)
    quote.delete()

    next_url = request.POST.get('next', 'quotes:root')

    return redirect(next_url)