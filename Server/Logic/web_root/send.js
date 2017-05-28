
// Constants
POST_SERVER_DIR = "request_song";
BAD_COLOR = "#ffdd00";
GOOD_COLOR = "#7ac143";

// Init it
$("#inform").hide();

/*
 * This function receives a message, and displays it to the user.
 * If isGood == true, then it will be green. Otherwise, red.
 */
function inform(msg, isGood) {
    informObj = $("#inform");

    // Change back color
    if (isGood) informObj.css("background", GOOD_COLOR);
    else informObj.css("background", BAD_COLOR);

    // Change text
    informObj.html(msg);

    // Animate
    informObj.slideDown().delay(4000).slideUp();
}

/*
 * This function checks if a value is valid. It returns true/false accordingly,
 * and informs the user if it is bad.
 * value: The given value
 * name: the name of the input
 */
function validate(value, name) {
    if(value.trim().length > 0)
        return true;
    inform("The required field '" + name + "' is empty. Please fill it.", false);
    return false;
}

$('form').submit(function(e){
    e.preventDefault();

    // Get input
    var name = $("input[name='name']").val();
    var videoUrl = $("input[name='video-url']").val();

    // Validate input
    if(!validate(name, "name") || !validate(videoUrl, "video url"))
        return;

    // Build params string
    var paramsAsJson = JSON.stringify({ "name": name, "video-url": videoUrl });

    // Send the post request
    $.ajax({
        type: "POST",
        url: POST_SERVER_DIR,

        contentType: "application/json; charset=utf-8",

        data: paramsAsJson,

        success: function(data) {
            inform("Successfully requested song!", true);
            // Clear the video url
            $("input[name='video-url']").val("");
        },
        error: function(xhr, ajaxOptions, thrownError){
            inform("[" + xhr.status + "] An error occurred: " + thrownError, false);
        }
    });

});
