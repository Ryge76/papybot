import {createMap} from './gmaps.js';

const formElt = document.getElementById("query");
const waitElt = document.getElementById("wait");
const questionListElt = document.getElementById("chat");
const visitorClasses = ["visitor", "shadow", "my-md-2", "list-group-item", "list-group-item-warning"];
const robotClasses = ["robot", "shadow", "my-md-2", "text-right", "list-group-item", "list-group-item-success"];
const robotAlertClasses = ["robot", "shadow", "my-md-2", "text-right", "list-group-item", "list-group-item-danger"];

// create <li> element to be added
const createListElt = (content, classTags) => {
    let liElt = document.createElement("li");
    liElt.classList.add(...classTags);
    liElt.textContent = content;
    return liElt
}

// insert dialog elements to the chat
const addTextToChat = (content, classTags) => {
    let liElt = createListElt(content, classTags);
    questionListElt.insertAdjacentElement("afterbegin", liElt);
}

// insert map element to the chat
const addMapToChat = (content) => {
    console.log("Ajout de la carte à la conversation.");
    questionListElt.insertAdjacentElement("afterbegin", content);
}


// setting callback function to back-end server
const callHome = async (search) => {
    const response = await fetch('/search/', {
        method: 'POST',
        cache: 'no-store',
        mode: 'cors',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({query: search}),
    });
    return response
}

// display question asked in the chat
// formElt.addEventListener("change", function(e){
//     let queryText = "";
//     queryText = e.target.value;
//     addTextToChat(queryText, visitorClasses);
// });


// handle form submission 
formElt.addEventListener("submit", function(e) {
    console.log("Formulaire validé");
    e.preventDefault()
    let searchText = "";
    searchText = formElt.elements.search.value;
    console.log("La valeur reçue: ", searchText);

    // TODO function to animate waiting phase
    addTextToChat(searchText, visitorClasses);
    addTextToChat("Laisse moi y réfléchir...", robotClasses);
    waitElt.classList.toggle("invisible");

    // text passed to back-end
    console.log("Appel de la fonction au backend via callHome");
    callHome(searchText)
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
            waitElt.classList.toggle("invisible");
            let sentence = "";

            if (answer['greetings']) {
                sentence = answer['greeting_word'] + " !\n";
            }

            if (answer['notsure']) {
                // TODO: function to generate various hesitation expressions
                sentence += "Hmm... \nCe que je sais c'est que " + answer['wikipedia'].extract;
                sentence += "\n Si tu veux en savoir plus: " + answer['wikipedia'].url;
                
                let mapElt = createMap(answer['gmaps'].coord);
                addMapToChat(mapElt);
                // createMap(answer['gmaps'].coord);
                addTextToChat(sentence, robotClasses);
                return
            }

            if (answer['rephrase']) {
                sentence += "Désolé, je n'ai pas compris ta demande... \n Pourrais-tu la reformuler autrement ? \n";
                return addTextToChat(sentence, robotAlertClasses);
            }

            // TODO: function to generate various ok response
            sentence += "Je connais bien " + answer['searched_word'] + ". \n";
            sentence += "L'adresse pour t'y rendre c'est: " + answer['gmaps'].address;
            
            let mapElt = createMap(answer['gmaps'].coord);         
            addMapToChat(mapElt);
            addTextToChat(sentence, robotClasses);
        })
        .catch((error) => {
            waitElt.classList.toggle("invisible");
            addTextToChat("Je suis désolé, ma réflexion n'a pas abouti... Peux tu reformuler ta demande ?", robotAlertClasses);
            console.error("Quelque chose s'est mal passé: ", error);
        })
        .finally(() => {
            formElt.elements.search.value="";
        });
});
