// this code will be run when the page loads
var KEY = 'TESTKEY';
var url = 'https://8.8.8.8/'; // replace this with the server ip or url
var request = new XMLHttpRequest();
request.open('GET', url + 'Video/' + KEY);
request.responseType = 'text'; // we are expecting JSON
request.onload = function() {
    // this is what happens when we get a response
    // parse the JSON, then display the YT video
    // the response is in: request.response;
    // we will update the display in this block
    var start = 0.0;
    var end = 10.0;
    var id = 'M7lc1UVf-VE';

    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    var player;
    function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
	    height: '390',
	    width: '640',
	    videoId: id,
	    events: {
		'onReady': onPlayerReady,
		'onStateChange': onPlayerStateChange
	    }
	});
    }

    player.seekTo(start,true);
};
request.send();
