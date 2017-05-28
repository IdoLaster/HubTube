function on_received_data(obj){
    $("#video-loading").fadeOut();
    $("#video-loaded").fadeIn();

    if(first_vid_id == null)
        init(obj["video-id"]);
    else {
        player.loadVideoById(obj["video-id"]);
        $("#player").fadeIn();
    }

    $("#song-name").html(obj["video-id"]);
    $("#player-name").html(obj["name"]);
}
