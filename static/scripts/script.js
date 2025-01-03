const searchForm = document.getElementById("searchForm");
searchForm.addEventListener("keydown",function(event) {
    if (event.key == "enter") {
        $.ajax({
            url: "/processSearch",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"result":searchForm.value}),
            success: function(response) {
                // successful response goes here
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
})