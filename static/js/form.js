const formElt = document.getElementById("query");
const questionListElt = document.getElementById("test");

// create <li> element to be added
const addListElt = (content) => {
    let liElt = document.createElement("li");
    liElt.classList.add("visitor");
    liElt.textContent = content;
    return liElt
}

formElt.addEventListener("change", function(e){
    let queryText = "";
    queryText = e.target.value;
    let liToAdd = addListElt(queryText);
    questionListElt.appendChild(liToAdd);
});


