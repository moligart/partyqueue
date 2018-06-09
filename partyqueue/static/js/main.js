var audio_player, mute;

$(document).ready(function() {
	$('span.glyphicon-search').on('click', function(event) {
	    $("#search_form").submit();
	});

	$('span.glyphicon-menu-hamburger').on('click', function(event) {
		$('nav').toggleClass('toggled');
		$('div.masthead').toggleClass('toggled');
	});

	audio_player = $('#sc_audio').get(0);
	if (audio_player) {
		audio_player.onended = function() {
			do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'music'}, '/remove/', delete_music_success, 'POST');
		}
	}
});

function do_post(data, url, func, type) {
	$.ajax({
		url: url,
		type: type,
		data: data,
		success : function(response) {
			console.log(func);
			console.log(response.text);
			func(response);
		},
		error : function(xhr, error_message, error) {
			console.log(xhr);
			console.log(error_message);
			console.log(error);
		}
	});
}

function default_success(response) {
	console.log(response);
}

function show_success(response) {
	if (response.video_id) {
		$('span[data-videoid="' + response.video_id + '"]').toggleClass('queued').text('In Queue');
	}
}

function play_callback(response) {
	current_id = response.item;
	tag = document.createElement('script');
	tag.src = "https://www.youtube.com/player_api";
	firstScriptTag = document.getElementsByTagName('script')[0];
	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
	showInfoBox('div.info_box.left', response.name);
}

//handles next video
function play_video_callback(response) {
	if (response.item) {
		player.loadVideoById(response.item);
		showInfoBox('div.info_box.left', response.name);
	}
}

function play_music_callback(response) {
	$(audio_player).attr('src', response.item);
	audio_player.play();
	showInfoBox('div.info_box.right', response.name);
}

function delete_video_success(response) {
	do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'video'}, '/play/', play_video_callback, 'POST');
}

function delete_music_success(response) {
	do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'music'}, '/play/', play_music_callback, 'POST');
}

function onYouTubeIframeAPIReady() {
		var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
		var height = (window.innerHeight > 0) ? window.innerHeight : screen.height;
		player = new YT.Player('youtube_player', {
		height: height,
		width: width,
		videoId: current_id,
		playerVars: { 
			'autoplay': 1, 
			'controls': 0,
			'cc_load_policy': 0,
			'modestbranding': 1,
			'playsinline': 0,
			'showinfo': 0
		},
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
		}
	});
}

function onPlayerReady(event) {
	if (mute)
		event.target.mute();

	event.target.playVideo();
	launchIntoFullscreen();
}

function onPlayerStateChange(event) {
	if (player.getPlayerState() == 0) {
		do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'video'}, '/remove/', delete_video_success, 'POST');
	}
}

function stopVideo() {
	player.stopVideo();
}

function init_video() {
	do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'video'}, '/play/', play_callback, 'POST');
}

function init_music() {
	do_post({'csrfmiddlewaretoken' : token, 'item_type' : 'music'}, '/play/', play_music_callback, 'POST');
}

function showInfoBox(sel, name)
{
	var elem = $(sel);
	var info_detail = $(elem).find('.info_detail')[0];
	$(info_detail).text(name);
	$(elem).addClass('fade_in');

	setTimeout(function() {
		$(elem).removeClass('fade_in');
	}, 3000);
}

function launchIntoFullscreen(a, b) {
	var element = document.documentElement;
	if(element.requestFullscreen) {
		element.requestFullscreen();
	} else if(element.mozRequestFullScreen) {
		element.mozRequestFullScreen();
	} else if(element.webkitRequestFullscreen) {
		element.webkitRequestFullscreen();
	} else if(element.msRequestFullscreen) {
		element.msRequestFullscreen();
	}

	$('div.cover').toggleClass('full');

	mute = (a && b);
	
	if (a)
		init_video();
	if (b)
		init_music();
}