//Scripts for the question page
//Scripts for Youtube Music Video
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
	origin : window.location.origin,
	});
}
function myFunction(start_time,play_time){
	player.setVolume(50)
	player.playVideo()
	player.seekTo(start_time)
	setTimeout(function(){ player.pauseVideo(); }, (play_time * 1000));
}
document.getElementById("hider").style.display = "none";

//Scripts for changing next question button to submit quiz on final question
{% if current_question+1 == question_list|length %}
	document.getElementById("submit_answer").value = "Submit Quiz"
{% endif %}
