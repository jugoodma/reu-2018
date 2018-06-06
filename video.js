// this code will be run when the page loads
var KEY = 'TESTKEY';
var url = 'https://8.8.8.8/'; // replace this with the server ip or url
var request = new XMLHttpRequest();
request.open('GET', url + 'Video/' + KEY);
request.responseType = 'text'; // we are expecting JSON
request.onload = function() {
    // this is what happens when we get a response
    // parse the JSON, then display the YT video
    // we will update the display in this block
    var res = JSON.parse(request.response); // example response: '{"id":"M7lc1UVf-VE","start":0.0,"end":10.0,"labels":"some, labels, here"}'

    // create the youtube video
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    var player;
    function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
	    height: '390',
	    width: '640',
	    videoId: res.id,
	    start: res.start,
	    end: res.end,
	    events: {
		'onReady': onPlayerReady,
		'onStateChange': onPlayerStateChange
	    }
	});
    }
    player.seekTo(start,false);
};
request.send();
