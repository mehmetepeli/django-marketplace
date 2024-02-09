from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

@login_required
def new_conversation(request, id):
    item = get_object_or_404(Item, id=id)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', id=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', id=id)
    else:
        form = ConversationMessageForm()

    context = {
        'form': form
    }

    return render(request, 'conversation/new.html', context)

@login_required
def inbox (request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    context = {
        'conversations': conversations
    }

    return render(request, 'conversation/inbox.html', context)

@login_required
def detail(request, id):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(id=id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', id=id)
    else:
        form = ConversationMessageForm()

    context = {
        'conversation': conversation,
        'form': form
    }

    return render(request, 'conversation/detail.html', context)