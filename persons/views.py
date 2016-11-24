from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse, HttpResponse
from .models import Person
from django.db.models import Count,Q
from .serializer import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .eloquent.person_e import Person as Person_e


class Persons:

    @require_http_methods(['GET'])
    def persons_list(request):
        return  render(request,'persons_list.html',{})

    @require_http_methods(['GET'])
    def json_search(request):
        # prepare sort params
        sort_list = ['created_at','comments__count']

        sort = request.GET.get('sort','created_at')
        reverse = request.GET.get('reverse','DESC')

        if (reverse != 'DESC' and reverse != 'ASC'):
            reverse = 'DESC'

        if sort not in sort_list:
            sort = 'created_at'

        if reverse == 'DESC':
            sort = '-'+sort

        result = Person.objects.annotate(Count('comments')).prefetch_related('comments').order_by(sort)

        # search request
        q = request.GET.get('q', '')
        if q:
          result = result.filter(Q(first_name__icontains = q) | Q(last_name__icontains = q) | Q(address__icontains = q) | Q(phone__icontains = q))

        #prepare pagination limit
        try:
            limit = int(request.GET.get('limit',10))
        except:
            limit=10

        #start paginate
        paginator = Paginator(result, limit)
        page = request.GET.get('page')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        #serialize data for json response
        count = paginator.count
        result = serialize(result)

        return JsonResponse({'data': result, 'count' : count},safe=False)

    @require_http_methods(['GET'])
    def json_search_eloquesnt(request):
        try:
            page = int(request.GET.get('page',1))
        except:
            page=1

        persons = Person_e.with_('last_comment').paginate(2,page)

        #persons2 = db.table('persons_comment').get()

        return JsonResponse({
            'count' : persons.total,
            'data'  : persons.to_dict()
        },content_type="application/json; charset=utf-8")




