from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json
from .models import Poll, Vote


# Create your views here.

def wrap_exceptions(view):
    def _wrapped_view(request, *args, **kwargs):
        try:
            result = view(request, *args, **kwargs)
        except Exception as e:
            result = {'error': repr(e)}

        return HttpResponse(json.dumps(result), content_type='application/json')

    return _wrapped_view


@wrap_exceptions
@require_POST
def create(request):
    data = json.loads(request.body.decode('utf-8'))

    poll = Poll.objects.create(
        name=data['name'],
        options=data['options']
    )

    return {'id': poll.pk}


@wrap_exceptions
@require_POST
def vote(request, id):
    data = json.loads(request.body.decode('utf-8'))

    poll = Poll.objects.get(pk=id)
    options = poll.options.split(',')

    option = options[int(data['option'])]

    vote = Vote.objects.create(
        poll=poll,
        option=option,
        ip=data['ip']
    )

    return {'id': vote.pk}


@wrap_exceptions
def results(request, id):
    poll = Poll.objects.get(pk=id)
    options = poll.options.split(',')

    queries = {
        'unique': '''select p.*, v.option, count(v.id) count
            from polls_poll p
            left join
                (select poll_id, max(id) max from polls_vote group by poll_id, ip) m
                on p.id = m.poll_id
            left join polls_vote v on m.max = v.id
            where p.id = %s
            group by v.option''',
        'raw': '''select p.*, v.option, count(v.id) count
            from polls_poll p
            left join polls_vote v on p.id = v.poll_id
            where p.id = %s
            group by v.option''',
    }

    options_count = {
        'unique': {str(x.option): x.count for x in Poll.objects.raw(queries['unique'], [id])},
        'raw': {str(x.option): x.count for x in Poll.objects.raw(queries['raw'], [id])},
    }

    return [
        {
            'name': option,
            'votes': options_count['raw'].get(option) or 0,
            'unique_votes': options_count['unique'].get(option) or 0,
        }
        for option in options]
