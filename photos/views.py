import json
from datetime import timedelta, datetime
from os.path import splitext, basename
from urllib.parse import urlparse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from photos import models
from photos.models import Photo, Like, Flag


def best(request, interval):
    if interval == 'all':
        likes_from = datetime.min
    else:
        likes_from = datetime.now() - timedelta(days=INTERVAL_DAYS[interval])

    all_photos = Photo.objects.filter(
        Q(like__created__gte=likes_from) | Q(like__created__isnull=True)
    ).annotate(likes=Count('like')).order_by('-likes')
    print(all_photos.query)

    photos = paginate(all_photos, request.GET.get('page'))

    context = {
        'photos': photos,
        'interval': interval
    }

    return render(request, 'best.html', context)


def new(request):
    all_photos = Photo.objects.annotate(likes=Count('like')).all().order_by('-created')

    photos = paginate(all_photos, request.GET.get('page'))

    context = {
        'photos': photos
    }

    return render(request, 'new.html', context)


def categories(request):
    all_photos = Photo.objects.annotate(likes=Count('like')).order_by('-likes')

    photos = paginate(all_photos, request.GET.get('page'))

    context = {
        'photos': photos
    }

    return render(request, 'categories.html', context)


def category_detail(request, category_id):
    all_photos = Photo.objects.filter(
        category_id=category_id
    ).annotate(likes=Count('like')).all().order_by('-likes')

    photos = paginate(all_photos, request.GET.get('page'))

    context = {
        'category_id': category_id,
        'photos': photos
    }

    return render(request, 'categories.html', context)


def items(request):
    url = request.GET.get('url')

    if url is not None:
        disassembled = urlparse(url)
        filename, _ = splitext(basename(disassembled.path))
        item_id = filename

        if item_id is not None:
            return redirect('/item/' + item_id)

    context = {
    }

    return render(request, 'items.html', context)


def item_detail(request, item_id):
    all_photos = Photo.objects.filter(
        item_id=item_id
    ).annotate(likes=Count('like')).all().order_by('-created')

    photos = paginate(all_photos, request.GET.get('page'))

    context = {
        'item_id': item_id,
        'photos': photos
    }

    return render(request, 'item_detail.html', context)


def detail(request, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    related_photos = Photo.objects.filter(
        feedback_id=photo.feedback_id
    ).annotate(likes=Count('like')).order_by('-likes')

    context = {
        'photo': photo,
        'photos': related_photos
    }

    return render(request, 'detail.html', context)


def like(request):
    if request.method == 'POST':
        photo_id = int(request.POST.get('photo_id'))
        session_key = get_session_key(request)

        like_object, created = Like.objects.get_or_create(
            session_key=session_key,
            photo_id=photo_id
        )

        if not created:
            like_object.delete()

        like_count = Like.objects.filter(photo_id=photo_id).count()
        return HttpResponse(str(like_count))

    return HttpResponse('error')


def flag(request):
    if request.method == 'POST':
        photo_id = int(request.POST.get('photo_id'))
        session_key = get_session_key(request)

        Flag.objects.get_or_create(
            session_key=session_key,
            photo_id=photo_id
        )

        return HttpResponse('ok')

    return HttpResponse('error')


def add_photos(request):
    return render(request, 'add_photos.html')


@csrf_exempt
def send_photos(request):
    if request.method == 'POST':
        package = json.loads(request.body.decode('utf-8'))
        feedbacks = package['feedbacks']
        category_id = package['categoryId']
        product_id = package['productId']

        for feedback in feedbacks:
            for image in feedback['images']:
                photo = Photo(
                    url=image['url'],
                    width=image['width'],
                    height=image['height'],
                    item_id=product_id,
                    category_id=category_id,
                    feedback_id=feedback['feedbackId'],
                )
                try:
                    photo.save()
                except Exception:
                    pass

    response = HttpResponse("OK")
    add_access_control_headers(response)
    return response


def get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def paginate(items, current_page):
    paginator = Paginator(items, 100)

    try:
        page = paginator.page(current_page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def add_access_control_headers(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


INTERVAL_DAYS = {
    'day': 1,
    'week': 7,
    'month': 30
}
