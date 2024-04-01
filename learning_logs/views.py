from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_log/index.html')

@login_required
def topics(request):
    """Shows all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    content = {'topics': topics}
    return render(request, 'learning_log/topics.html', content)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by('-date_added')
    content = {'topic': topic, 'entries': entries}
    return render(request, 'learning_log/topic.html', content)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid:
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return redirect('learning_logs:topics')
        
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

@login_required
def edit_entry(request, entry_id):
    """Editing an existing entry."""
    entry = Entry.objects.get(id=entry_id) 
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry' : entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log/edit_entry.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid:
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_log/new_entry.html', context)