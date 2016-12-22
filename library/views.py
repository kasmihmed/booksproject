from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from library.models import Book,Genre
from library.serializers import BookSerializer,GenreSerializer
# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def book_list(request):
    """
    List all Books from the authenticated user
    """
    if request.method == 'GET':
        # check if the user is authenticated otherwise redirect to login page
        if request.user.is_authenticated:
            books = Book.objects.filter(author=request.user)
            serializer = BookSerializer(books, many=True)
            return JSONResponse(serializer.data)
        else:
            return redirect('/login/?next=/books/')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            if Book.objects.filter(author=request.user).count()>=5:
                return JSONResponse({'error':'you reached your free account limit'}, status=400)
            data = JSONParser().parse(request)
            serializer = BookSerializer(data=data,context={'request': request})
            if serializer.is_valid():
                if Book.objects.filter(author=request.user, title=data['title']).exists():
                    return JSONResponse({"error": "there is a conflict, you already have a book with that title"},
                                        status=409)
                else:
                    serializer.save()
                    return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
        else:
            return redirect('/login/?next=/books/')
    else:
        return JSONResponse({'error':'method not supported'}, status=405)

@csrf_exempt
def genre_list(request):
    """
        List all Genres from the authenticated user
        """
    if request.method == 'GET':
        # check if the user is authenticated otherwise redirect to login page
        if request.user.is_authenticated:
            genres = Genre.objects.all()
            serializer = GenreSerializer(genres, many=True)
            return JSONResponse(serializer.data)
        else:
            return redirect('/login/?next=/genres/')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            data = JSONParser().parse(request)
            serializer = GenreSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)
        else:
            return redirect('/login/?next=/genres/')
    else:
        return JSONResponse({'error': 'method not supported'}, status=405)


@csrf_exempt
def book_detail(request, slug):
    """
    Retrieve, update or delete a Book .
    """
    try:
        book = Book.objects.get(slug=slug)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            if request.user.id == book.author_id:
                data = JSONParser().parse(request)
                serializer = BookSerializer(book, data=data,context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data)
                return JSONResponse(serializer.errors, status=400)
            else:
                return JSONResponse({'error':'you do not have  the right permissions to update this book'},
                                    status=400)
        else:
            return redirect('/login/?next=/books/{}/'.format(slug))

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)
    else:
        return JSONResponse({'error': 'method not supported'}, status=405)

@csrf_exempt
def add_genre(request,book_slug,genre_slug):
    """
        add a new genre to a  Book .
    """
    try:
        book = Book.objects.get(slug=book_slug)
    except Book.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.id == book.author_id:
                if book.genres.filter(slug=genre_slug).exists():
                    return JSONResponse({'error': 'the genre already exist'}, status=409)
                else:
                    try:
                        genre = Genre.objects.get(slug=genre_slug)
                        book.genres.add(genre)
                        book.save()
                        return JSONResponse(BookSerializer(book).data, status=201)
                    except Genre.DoesNotExist:
                        return JSONResponse({'error':'genre does not exist'}, status=404)
            else:
                return JSONResponse({'error': 'you do not have  the right permissions to update this book'},
                                    status=400)
        else:
            return redirect('/login/?next=/books/{}/'.format(book_slug))
    else:
        return JSONResponse({'error': 'method not supported'}, status=405)