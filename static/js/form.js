import {gmapsCall, mapsKey, createMap, getCoordinates, createMapElt} from './gmaps';

const formElt = document.getElementById("query");
const questionListElt = document.getElementById("test");

// create <li> element to be added
const createListElt = (content, category) => {
    let liElt = document.createElement("li");
    liElt.classList.add(category);
    liElt.textContent = content;
    return liElt
}

// insert dialog elements to the chat
const addTextToChat = (content, category) => {
    let liElt = createListElt(content, category);
    questionListElt.insertAdjacentElement("afterbegin", liElt);
}

// insert map elements to the chat
const addMapToChat = (content) => {
    questionListElt.insertAdjacentElement("afterbegin", liElt);
}

// setting callback function to back-end server
const callHome = async (search) => {
    await fetch('/search/', {
        method: 'POST',
        cache: 'no-store',
        mode: 'cors',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({query: search}),
    })
        .then((response) => {
            if (response.status === 200) {
                console.log("Back-end a répondu: Rock'n Roll Baby !");

                let answer = response.json()
                console.log("La réponse: \n", answer);
                return answer
            }
            else {
                // TODO handle other type of error + catch() function
                console.log("Try again: ", response.statusText);
                throw error
            }
        })
        .then((answer) => {
            console.log("On passe à la création des phrases réponses.")
            let sentence = "";

            if (answer['greetings']) {
                sentence = answer['greeting_word'] + " !\n";
            }

            if (answer['notsure']) {
                // TODO: function to generate various hesitation expressions
                sentence += "Hmm, j'hésite... \nCe que je sais c'est que " + answer['wikipedia'].extract;
                sentence += "\n Si tu veux en savoir plus: " + answer['wikipedia'].url
                return addTextToChat(sentence, 'robot');
            }

            if (answer['rephrase']) {
                sentence += "Désolé, je n'ai pas compris ta demande... \n Pourrais-tu la reformuler autrement ? \n";
                return addTextToChat(sentence, 'robot');
            }

            // TODO: function to generate various ok response
            sentence += "Je connais bien " + answer['searched_word'] + ". \n";
            sentence += "L'adresse pour t'y rendre c'est: " + answer['gmaps'].address
            return addTextToChat(sentence, 'robot');
        })
        .catch((error) => {
            console.error("Quelque chose s'est mal passé: ", error);
        });
}


// display question asked in the chat
formElt.addEventListener("change", function(e){
    let queryText = "";
    queryText = e.target.value;
    addTextToChat(queryText, "visitor")
});

// handle form submission 
formElt.addEventListener("submit", function(e) {
    console.log("Formulaire validé");
    e.preventDefault()
    let searchText = "";
    searchText = formElt.elements.search.value;
    console.log("La valeur reçue: ", searchText);

    // TODO function to animate waiting phase
    addTextToChat("Laisse moi y réfléchir...", "robot");

    // text passed to back-end
    console.log("Appel de la fonction au backend via callHome");
    callHome(searchText) 
});


