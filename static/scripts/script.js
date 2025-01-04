const searchForm = document.getElementById("searchForm");
const searchResultDiv = document.getElementById("searchResultDiv");
searchForm.addEventListener("keydown",function(event) {
    if (event.key == "enter") {
        $.ajax({
            url: "/processSearch",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"result":searchForm.value}),
            success: function(response) {
                let searchList = response.result;

                let card = document.createElement("div");
                card.className = "card cardDiv m-auto w-50 mt-1";

                let clickablility = document.createElement("a");
                clickablility.href = "";
                clickablility.className = "text-decoration-none";

                let image = document.createElement("img");
                image.src = "";
                image.className = "card-img-top w-50 m-auto pt-1";

                let cardBody = document.createElement("div");
                cardBody.className = "card-body text-center";

                let cardText = document.createElement("p");
                cardText.innerHTML = "";
                cardText.className = "card-text searchCardText";
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
})