from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from .models import Person
from django.db.models import Count
from .serializer import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Persons:
    @require_http_methods(['GET'])
    def persons_list(request):
         return  render(request,'persons_list.html',{})

    @require_http_methods(['GET'])
    def json_search(request):

        result = Person.objects.annotate(Count('comments')).prefetch_related('comments')

        page = request.GET.get('page')
        paginator = Paginator(result, 10)

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        result = serialize(result)

        return JsonResponse(result,safe=False)



