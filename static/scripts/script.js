const searchForm = document.getElementById("searchForm");
const searchResultDiv = document.getElementById("searchResultDiv");

var searchResultsShowing = false;

searchForm.addEventListener("keydown",function(event) {
    if (event.key == "Enter") {
        event.preventDefault();

        while (searchResultDiv.firstChild) {
            searchResultDiv.removeChild(searchResultDiv.lastChild);
        };

        searchResultsShowing = false;

        $.ajax({
            url: "/processSearch",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"result":searchForm.value}),
            success: function(response) {
                var searchList = response.result.slice(0,2);

                var cardList = searchList.map(item => {
                    let card = document.createElement("div");
                    card.className = "card cardDiv m-auto w-50 mt-1 mb-1";

                    let clickablility = document.createElement("a");
                    clickablility.href = `/product/${item["productID"]}`;
                    clickablility.className = "text-decoration-none";

                    let image = document.createElement("img");
                    image.src = `../static/images/${item["productImageName"]}`;
                    image.className = "card-img-top w-50 m-auto pt-1";

                    let cardBody = document.createElement("div");
                    cardBody.className = "card-body text-center";

                    let cardText = document.createElement("p");
                    cardText.innerHTML = `${item["productName"]} $ ${item["productPrice"]}`;
                    cardText.className = "card-text searchCardText";

                    cardBody.appendChild(cardText);
                    clickablility.appendChild(image);
                    clickablility.appendChild(cardBody);
                    card.appendChild(clickablility);

                    return card;
                })

                for (let i = 0; i < cardList.length; i++) {
                    searchResultDiv.appendChild(cardList[i]);
                };

                searchResultsShowing = true;

            },
            error: function(error) {
                console.log(error);
            }
        });
    }
})

document.body.addEventListener("click", function() {
    if (searchResultsShowing) {
        while (searchResultDiv.firstChild) {
            searchResultDiv.removeChild(searchResultDiv.lastChild);
        };

        searchResultsShowing = false;
    }
})

function addToCart(id) {
    $.ajax({
        url: "/addToCart",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"productID":id}),
        success: function(response) {
           if (response) {
                document.getElementById("cartStatusDiv").classList.add("show");
                
                setTimeout(() => {
                    document.getElementById("cartStatusDiv").classList.remove("show")
                },3000)
           }
        },
        error: function(error) {
            console.log(error);
        }
    });
}