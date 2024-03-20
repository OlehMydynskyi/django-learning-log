from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('learning_logs:topics')
        
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

def edit_entry(request, entry_id):
    """Editing an existing entry."""
    entry = Entry.objects.get(id=entry_id) 
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry' : entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log/edit_entry.html', context)

def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

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