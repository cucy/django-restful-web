from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from toys.models import Toy
from toys.serializers import ToySerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super().__init__(content, **kwargs)


@csrf_exempt
def toy_list(request):
    if request.method == "GET":
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return JSONResponse(toys_serializer.data)

    if request.method == "POST":
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(data=toy_data)

        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data,
                                status=status.HTTP_201_CREATED)
        
        return JSONResponse(toy_serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def toy_detail(request, pk):
    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        toy_serializer = ToySerializer(toy)
        return JSONResponse(toy_serializer.data)

    if request.method == 'PUT':
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(toy, data=toy_data)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data)
        
        return JSONResponse(toy_serializer.errors,
                            status = status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        toy.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


"""
(sx3.5.3) ➜  restful01 git:(master) ✗ curl localhost:8000/toys/
[{"pk":2,"name":"Hawaiian Barbie","description":"Barbie loves Hawaii","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Dolls","was_included_in_home":true},{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Action figures","was_included_in_home":false}]%

 curl -X GET localhost:8000/toys/
[{"pk":2,"name":"Hawaiian Barbie","description":"Barbie loves Hawaii","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Dolls","was_included_in_home":true},{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Action figures","was_included_in_home":false}]


 curl -iX GET localhost:8000/toys/
HTTP/1.0 200 OK
Date: Sun, 25 Mar 2018 07:50:47 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 365

[{"pk":2,"name":"Hawaiian Barbie","description":"Barbie loves Hawaii","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Dolls","was_included_in_home":true},{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Action figures","was_included_in_home":false}]%


 http :8000/toys/
HTTP/1.0 200 OK
Content-Length: 365
Content-Type: application/json
Date: Sun, 25 Mar 2018 07:51:44 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN

[
    {
        "description": "Barbie loves Hawaii",
        "name": "Hawaiian Barbie",
        "pk": 2,
        "release_date": "2018-03-25T07:13:26.480780Z",
        "toy_category": "Dolls",
        "was_included_in_home": true
    },
    {
        "description": "Snoopy speaks five languages",
        "name": "Snoopy talking action figure",
        "pk": 1,
        "release_date": "2018-03-25T07:13:26.480780Z",
        "toy_category": "Action figures",
        "was_included_in_home": false
    }
]



   http -b :8000/toys/
[
    {
        "description": "Barbie loves Hawaii",
        "name": "Hawaiian Barbie",
        "pk": 2,
        "release_date": "2018-03-25T07:13:26.480780Z",
        "toy_category": "Dolls",
        "was_included_in_home": true
    },
    {
        "description": "Snoopy speaks five languages",
        "name": "Snoopy talking action figure",
        "pk": 1,
        "release_date": "2018-03-25T07:13:26.480780Z",
        "toy_category": "Action figures",
        "was_included_in_home": false
    }
]



# ------- detail
http :8000/toys/1

HTTP/1.0 200 OK
Content-Length: 197
Content-Type: application/json
Date: Sun, 25 Mar 2018 07:55:08 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN

{
    "description": "Snoopy speaks five languages",
    "name": "Snoopy talking action figure",
    "pk": 1,
    "release_date": "2018-03-25T07:13:26.480780Z",
    "toy_category": "Action figures",
    "was_included_in_home": false
}


curl -iX GET localhost:8000/toys/1
HTTP/1.0 200 OK
Date: Sun, 25 Mar 2018 07:55:48 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 197

{"pk":1,"name":"Snoopy talking action figure","description":"Snoopy speaks five languages","release_date":"2018-03-25T07:13:26.480780Z","toy_category":"Action figures","was_included_in_home":false}%


# 404 --->>>>>
http :8000/toys/3

HTTP/1.0 404 Not Found
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Sun, 25 Mar 2018 07:53:11 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN

curl -iX GET localhost:8000/toys/3

HTTP/1.0 404 Not Found
Date: Sun, 25 Mar 2018 07:54:13 GMT
Server: WSGIServer/0.2 CPython/3.5.3
Content-Length: 0
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN



# ---- POST ----
 http POST :8000/toys/ name="PvZ 2 puzzle" description="Plants vs        Zombies 2 puzzle" toy_category="Puzzle" was_included_in_home=false     release_date="2017-10-08T01:01:00.776594Z"
 
HTTP/1.0 201 Created
Content-Length: 178
Content-Type: application/json
Date: Sun, 25 Mar 2018 07:57:10 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN

{
    "description": "Plants vs        Zombies 2 puzzle",
    "name": "PvZ 2 puzzle",
    "pk": 3,
    "release_date": "2017-10-08T01:01:00.776594Z",
    "toy_category": "Puzzle",
    "was_included_in_home": false
}

curl -iX POST -H "Content-Type: application/json" -d '{"name":"PvZ       2 puzzle", "description":"Plants vs Zombies 2 puzzle",        "toy_category":"Puzzle", "was_included_in_home": "false",     "release_date": "2017-10-08T01:01:00.776594Z"}'      localhost:8000/toys/

HTTP/1.0 201 Created
Date: Sun, 25 Mar 2018 07:58:15 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN
Content-Type: application/json
Content-Length: 177

{"pk":4,"name":"PvZ       2 puzzle","description":"Plants vs Zombies 2 puzzle","release_date":"2017-10-08T01:01:00.776594Z","toy_category":"Puzzle","was_included_in_home":false}%


# ---- PUT ---
# 全量更新
http PUT :8000/toys/4 name="PvZ 3 puzzle" description="Plants vs Zombies 3 puzzle" toy_category="Puzzles & Games" was_included_in_home=false release_date="2017-10-08T01:01:00.776594Z"

HTTP/1.0 200 OK
Content-Length: 180
Content-Type: application/json
Date: Sun, 25 Mar 2018 07:59:32 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN

{
    "description": "Plants vs Zombies 3 puzzle",
    "name": "PvZ 3 puzzle",
    "pk": 4,
    "release_date": "2017-10-08T01:01:00.776594Z",
    "toy_category": "Puzzles & Games",
    "was_included_in_home": false
}


curl -iX PUT -H "Content-Type: application/json" -d '{"name":"PvZ 3 puzzle", "description":"Plants vs Zombies 3 puzzle", "toy_category":"Puzzles & Games", "was_included_in_home": "false", "release_date": "2017-10-08T01:01:00.776594Z"}' localhost:8000/toys/4

HTTP/1.0 200 OK
Date: Sun, 25 Mar 2018 08:00:28 GMT
Server: WSGIServer/0.2 CPython/3.5.3
Content-Type: application/json
X-Frame-Options: SAMEORIGIN
Content-Length: 180

{"pk":4,"name":"PvZ 3 puzzle","description":"Plants vs Zombies 3 puzzle","release_date":"2017-10-08T01:01:00.776594Z","toy_category":"Puzzles & Games","was_included_in_home":false}

# 部分更新
http PUT :8000/toys/4 name="PvZ 4 puzzle"


curl -iX PUT -H "Content-Type: application/json" -d '{"name":"PvZ 4       puzzle"}' localhost:8000/toys/4

HTTP/1.0 400 Bad Request
Date: Sun, 25 Mar 2018 08:03:17 GMT
Server: WSGIServer/0.2 CPython/3.5.3
Content-Type: application/json
X-Frame-Options: SAMEORIGIN
Content-Length: 129

{"toy_category":["This field is required."],"release_date":["This field is required."],"description":["This field is required."]}%


# --- DELETE ---
 http DELETE :8000/toys/4
 
HTTP/1.0 204 No Content
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Sun, 25 Mar 2018 08:04:19 GMT
Server: WSGIServer/0.2 CPython/3.5.3
X-Frame-Options: SAMEORIGIN


curl -iX DELETE localhost:8000/toys/4

"""
