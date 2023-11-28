import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Article, Review
from django.db.models import Q, F, Count, Avg, Max

# Author.objects.get_authors_by_article_count()


def get_authors(search_name=None, search_email=None) -> str:
    query = Q()
    if search_name is not None and search_email is not None:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name is not None:
        query = Q(full_name__icontains = search_name)
    elif search_email is not None:
        query = Q(email__icontains=search_email)
    
    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors or (search_name is None and search_email is None):
        return ""

    return '\n'.join(f"Author: {a.full_name}, email: {a.email}, "\
                     f"status: {'Banned' if a.is_banned is True else 'Not Banned'}" 
                     for a in authors)


def get_top_publisher() -> str:
    author = Author.objects.get_authors_by_article_count().first()

    if not author or not author.article_count:
        return ""

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer() -> str:
    reviewer = Author.objects.prefetch_related('reviews').annotate(
        review_count = Count('reviews')
    ).order_by(
        '-review_count',
        'email'
    ).first()

    if not reviewer or not reviewer.review_count:
        return ""
    
    return f"Top Reviewer: {reviewer.full_name} with {reviewer.review_count} published reviews."



def get_latest_article() -> str:
    article = Article.objects.prefetch_related('reviews').annotate(
        num_reviews = Count('reviews'),
        avg = Avg('reviews__rating')
    ).last()
    
    if not article:
        return ""

    authors = ', '.join(a.full_name for a in article.authors.all().order_by('full_name'))
    avg = article.avg if article.avg else 0

    return f"The latest article is: {article.title}. "\
            f"Authors: {authors}. "\
            f"Reviewed: {article.num_reviews} times. "\
            f"Average Rating: {avg:.2f}."


def get_top_rated_article() -> str:
    article = Article.objects.prefetch_related('reviews').annotate(
        num_reviews = Count('reviews'),
        avg_rating = Avg('reviews__rating'),
        top_rating = Max('reviews__rating')
    ).filter(
        reviews__rating=F('top_rating')
    ).order_by(
        '-avg_rating',
        'title'
    ).first()

    if not article or article.num_reviews == 0:
        return ""

    return f"The top-rated article is: {article.title}, "\
        f"with an average rating of {article.avg_rating:.2f}, "\
        f"reviewed {article.num_reviews} times."


def ban_author(email=None) -> str:
    author = Author.objects.filter(email=email).first()

    if not author or email is None:
        return "No authors banned."

    author.is_banned = True
    author.save()

    review_cnt = author.reviews.count()

    for review in author.reviews.all():
        review.delete()
        author.save()

    return f"Author: {author.full_name} is banned! {review_cnt} reviews deleted."
