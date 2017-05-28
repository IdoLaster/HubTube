var player;
var first_vid_id = null;

function init(vid_id){
    first_vid_id = vid_id;

    //Some api stuff, just need to be here.
    var tag = document.createElement('script');

    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',

    //This videoId can be changed to have a other default video.
    videoId: first_vid_id,
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });

}

//Again, some api stuff, need to be here.
function onPlayerReady(event) {
  event.target.playVideo();
}

var done = false;
function onPlayerStateChange(event) {
  // This is the part we actually care about, here we can change the video when it's end
  // This V part of code we exectue each time a video will end.
  if(event.data == YT.PlayerState.ENDED){
      $("#player").fadeOut();
      get_next_song();
      $("#video-loaded").fadeOut();
      $("#video-loading").fadeIn();
  }
}
