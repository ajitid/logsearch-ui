from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'ws/logsearch/log_servers', consumers.LogServerConsumer),
    url(r'^ws/logsearch/results/(?P<uid>[\w\d-]+)/$',
        consumers.LogClientConsumer),
    # url(r'ws/logsearch/results/<uid>', consumers.LogClientConsumer),
]
