# booksproject

1 install required libraries
-----------------------------
>pip install -r requirement.txt
2 make migrations in case missing
----------------------------------
>./manage.py makemigrations
>./manage migrate
3 create super user
-------------------
>./manage.py createsuperuser
4 start the server and login
-----------------------------
>./manage.py runserver
login at:
/admin/login/?next=/books/

5 get all the books
-------------------
GET /books/
6 get all the genres
--------------------
GET /genres/
7 add a new book
---------------
POST /books/
request.body(json):
{"title":"your title"}
8 add a new genre:
-----------------
POST /genres/
request.body(json):
{"title":"your title"}
9 add a genre to a book
-----------------------
POST /books/$book_slug/genres/$genre_slug
10 update a book
----------------
PUT /books/$book_slug/
request.body(json):
{"title":"your new title"}
