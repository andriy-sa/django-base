from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse, HttpResponse
from .models import Person
from django.db.models import Count,Q
from .serializer import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .eloquent.person_e import Person as Person_e
from  blog.settings import DB as db
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
        #return render(request, 'persons_list.html', {})
        return JsonResponse({'data': result, 'count' : count},safe=False)

    @require_http_methods(['GET'])
    def json_search_eloquesnt(request):
        #prepare page param
        try:
            page = int(request.GET.get('page',1))
        except:
            page=1

        #prepare limit param
        try:
            limit = int(request.GET.get('limit',10))
        except:
            limit = 10

        #prepare offset
        offset = 0;
        if (page > 1):
            offset = limit * (page - 1)


        #prepare sort params
        sort_list = ['created_at', 'comments__count']

        sort = request.GET.get('sort', 'created_at')
        reverse = request.GET.get('reverse', 'DESC')

        if (reverse != 'DESC' and reverse != 'ASC'):
            reverse = 'DESC'

        if sort not in sort_list:
            sort = 'created_at'

        persons = Person_e.select('persons_person.*')\
            .where('persons_person.id','>',0)\

        #make search if q
        q = request.GET.get('q', '')
        if q:
            persons = persons.where(
                db.query().where('first_name', 'like', '%'+q+'%')\
                .or_where('last_name', 'like', '%'+q+'%')\
                .or_where('address', 'like', '%'+q+'%')\
                .or_where('phone', 'like', '%'+q+'%')
                )
        total_count = persons.count()

        persons = persons.add_select(db.raw('count(persons_comment.id) as comments__count'))\
            .with_('last_comment')\
            .left_join('persons_comment', 'persons_person.id', '=', 'persons_comment.person_id')\
            .order_by(sort, reverse)\
            .group_by('persons_person.id')\
            .limit(limit).offset(offset)\
            .get().serialize()

        return JsonResponse({
            'count' : total_count,
            'data'  : persons
        },content_type="application/json; charset=utf-8")




