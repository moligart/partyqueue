import json, random, utils

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.utils import timezone
from classes.youtube_service import youtube_search
from classes import soundcloud_service

from .models import QueueItem

# Create your views here.
def index(request):
	utils.set_uid(request)
	return render(request, 'partyqueue/home.html', {'title': ' - Home'})

def add(request):
	return utils.add(request)

def all(request):
	queue_item_list = QueueItem.objects.order_by('place_in_line')
	return render(request, 'partyqueue/all.html', {'title': ' - All', 'queue_items': QueueItem.objects.order_by('place_in_line')})

def play(request):
	return utils.play(request)

def remove(request):
	return utils.remove(request)

def watch(request):
	return render(request, 'partyqueue/watch.html', {'title': ' - Watch'})

def listen(request):
	return render(request, 'partyqueue/listen.html', {'title': ' - Listen'})

def mashup(request):
	return render(request, 'partyqueue/mashup.html', {'title': ' - Mashup'})