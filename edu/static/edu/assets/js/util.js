
// This will send the enquiry request to the server
function sendenquiry(){
    var domurl = document.URL;
    var splitList = domurl.split("/");
    var domain = splitList[0] + '//' + splitList[2];
	$.ajax({
        type: "POST",
        url: domain + "/account/enquiry/",
        data: $("#enquiry").serialize(),
        success: function (data, status) {
            $("#alertSuccess").css("display", "block"),
            $("#alertFailure").css("display", "none")},
        error: function (data, status) {
            $("#alertFailure").css("display", "block"),
            $("#alertSuccess").css("display", "none")},
    });
    
    // prevent from reloading the page
    return false
};