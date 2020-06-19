const formElt = document.getElementById("query");
const questionListElt = document.getElementById("test");

// create <li> element to be added
const addListElt = (content) => {
    let liElt = document.createElement("li");
    liElt.classList.add("visitor");
    liElt.textContent = content;
    return liElt
}

// setting callback function to back-end server

async const callHome = (search) => {

    await fetch('127.0.0.1/search/', {
        method: 'POST',
        cache: 'no-store',
        mode: 'cors',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(search),
    })
    .then((response) =>{
        if (response.status === 200) {
            console.log("Back-end a répondu: Rock'n Roll Baby !");
        }
        else {
            console.log("Try again: ", response.statusText);
        }
    })
}

formElt.addEventListener("change", function(e){
    let queryText = "";
    queryText = e.target.value;
    let liToAdd = addListElt(queryText);
    questionListElt.appendChild(liToAdd);
});

formElt.addEventListener("submit", function(e) {
    console.log("Formulaire validé");
    e.preventDefault()
    let searchText = "";
    searchText = form.elements.search.value;
    console.log(searchText);

    // passer la demande au back-end
    console.log("Appel de la fonction callHome");
    callHome(searchText);

    // 
} )


