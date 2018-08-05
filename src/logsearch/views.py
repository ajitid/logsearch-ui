from uuid import uuid4
from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils import redis
from utils.helpers import deserialize
from .consumer_helpers import send_to_group_sync


def index(request):
    if request.method == 'GET':
        log_query = request.GET.get('log_query')
        if log_query and log_query.strip():
            uid = str(uuid4())
            send_to_group_sync('log_servers', {
                'type': 'log_query',
                'uid': uid,
                'query': log_query
            })
            return redirect('results', uid)
    return render(request, 'logsearch/index.html')


def results(request, uid):
    return render(request, 'logsearch/results.html')


def log_servers(request):
    context = {
        'log_servers': deserialize(redis.get('log_servers'))
    }
    return render(request, 'logsearch/log_servers.html', context)


def log_servers_count(request):
    return JsonResponse({
        'count': len(deserialize(redis.get('log_servers')))
    })
