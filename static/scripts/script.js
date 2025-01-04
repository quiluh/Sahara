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

                var searchList = response.result;

                var cardList = searchList.map(item => {
                    let card = document.createElement("div");
                    card.className = "card cardDiv m-auto w-50 mt-1";

                    let clickablility = document.createElement("a");
                    clickablility.href = `/product/${item["productID"]}`;
                    clickablility.className = "text-decoration-none";

                    let image = document.createElement("img");
                    image.src = `/productImage/${item["productID"]}`;
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

            },
            error: function(error) {
                console.log(error);
            }
        });
    }
})