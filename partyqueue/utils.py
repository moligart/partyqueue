import json, random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.utils import timezone
from classes import soundcloud_service, youtube_service

from .models import QueueItem

def add(request):
	data = {'title': ' - Add'}
	if request.method == 'POST':
		if 'search_text' in request.POST:
			search_text = request.POST.get('search_text')
			results = youtube_service.youtube_search({'q': request.POST['search_text']})
			music_results = soundcloud_service.search(request.POST['search_text'])

			vid_ids = []
			for r in results:
				vid_ids.append(r['id']['videoId'])
			for m in music_results:
				vid_ids.append(m.id)

			already_queued = []
			queued_by_user = []
			for item in QueueItem.objects.filter(item_id__in=vid_ids):
				already_queued.append(item.item_id)
				if item.queued_by == request.session.get('uid'):
					queued_by_user.append(item.item_id)

			data['results_list'] = results
			data['music_results'] = music_results
			data['already_queued'] = already_queued
			data['queued_by_user'] = queued_by_user

		if 'operation' in request.POST:
			if 'video_id' in request.POST:
				is_music = ''
				if request.POST.get('is_music') == 'true':
					is_music = 'music'
				else:
					is_music = 'video'

				queue_item = QueueItem(item_name = request.POST.get('video_name'), 
					item_type = is_music,
					item_id = request.POST.get('video_id'), 
					queued_time = timezone.now(), 
					place_in_line = QueueItem.objects.all().count(),
					queued_by = request.session.get('uid'))

				queue_item.save()
				data['video_id'] = request.POST.get('video_id')
				return HttpResponse(json.dumps(data), content_type = 'application/json')

	return render(request, 'partyqueue/add.html', data)

def play(request):
	item_type = request.POST.get('item_type')
	item_to_queue = QueueItem.objects.filter(item_type = item_type).order_by('place_in_line')
	data = {}
	if item_to_queue:
		if item_type == 'music':
			data['item'] = soundcloud_service.getStreamableURL(item_to_queue[0].item_id)
			data['name'] = item_to_queue[0].item_name;
		else:
			data['item'] = item_to_queue[0].item_id
			data['name'] = item_to_queue[0].item_name;
	return HttpResponse(json.dumps(data), content_type = 'application/json')

def remove(request):
	item_type = request.POST.get('item_type')
	item_to_queue = QueueItem.objects.filter(item_type = item_type).order_by('place_in_line')
	if item_to_queue:
		item_to_queue[0].delete()
	return HttpResponse(json.dumps({}), content_type = 'application/json')

def set_uid(request):
	if not request.session.get('uid'):
		request.session['uid'] = random.randrange(0, 100000, 5)