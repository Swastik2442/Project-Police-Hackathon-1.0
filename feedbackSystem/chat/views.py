from django.shortcuts import render
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden, JsonResponse

from feedback.models import Division, PoliceStation, Feedback
from .models import Chat, Message
from .utils import bodyToDict

def index_view(request: HttpRequest):
    """A Django View for the Staff Dashboard."""
    uChat = None
    feedbacks = None
    user = request.user
    userIP = request.META.get('REMOTE_ADDR')
    if user.is_authenticated:
        uChat = Chat.objects.filter(user=user).first()
        feedbacks = Feedback.objects.filter(submittedBy=user).order_by('-feedbackDate')
    if uChat == None:
        uChat = Chat.objects.filter(userIP=userIP).first()
        feedbacks = Feedback.objects.filter(userIP=userIP).order_by('-feedbackDate')
        if uChat == None:
            if user.is_anonymous:
                user = None
            uChat = Chat.objects.create(user=user, userIP=userIP)
            uChat.save()
    messages = Message.objects.filter(chat=uChat).order_by("timestamp")
    divisions = Division.objects.all()
    return render(request, 'chat/index.html', {'chat': uChat, 'messages': messages, 'divisions': divisions, 'feedbacks': feedbacks})

def addMessage_API(request: HttpRequest, chatID: int):
    """A Django View for Handling adding messages to a Chat."""
    if request.method == 'GET':
        return HttpResponseNotAllowed(["POST"])
    
    uChat = Chat.objects.filter(id=chatID).first()
    if uChat == None:
        raise HttpResponseBadRequest("No such Chat found.")
    elif (uChat.user != None and uChat.user != request.user) and (uChat.userIP != request.META.get('REMOTE_ADDR')):
        return HttpResponseForbidden("You are not authorized to access this Chat.")
    
    requestDict = bodyToDict(request.body)
    message = requestDict.get('message', None)
    
    if message == None:
        return HttpResponseBadRequest("User Message not found.")
    
    error = True
    oldMessages = Message.objects.filter(chat=uChat).order_by("timestamp")
    response = {'type': 1, 'response': ""}

    return JsonResponse({'error': error, 'bot': response})