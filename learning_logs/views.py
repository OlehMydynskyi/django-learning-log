from django.shortcuts import render
from .models import Topic

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_log/index.html')

def topics(request):
    """Shows all topics."""
    topics = Topic.objects.order_by('date_added')
    content = {'topics': topics}
    return render(request, 'learning_log/topics.html', content)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    content = {'topic': topic, 'entries': entries}
    return render(request, 'learning_log/topic.html', content)