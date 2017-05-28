GET_SONG_URL = "request_song"
TRY_INTERVAL = 2000

/**
 * This function fetches from the server the next video to play, and
 *  returns it as an object of:
 *  {
 *      video-id : The id of the video
 *      name : name of sender
 *  }
 */
function get_next_song() {
    $.ajax({
        type: "GET",
        url: GET_SONG_URL,

        dataType: "json",

        success: function(data) {
            on_received_data(data);
        },
        error: function(xhr, ajaxOptions, thrownError){
            console.log("HRT " + xhr + " " + thrownError);
            setTimeout(get_next_song, TRY_INTERVAL);
        }
    });
}
