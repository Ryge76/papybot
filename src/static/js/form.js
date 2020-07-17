import {createMap} from './gmaps.js';
import {addTextToChat, addMapToChat, tellMoreAbout, robotCommunicates} from './dialogue.js'

const formElt = document.getElementById("query");
const waitElt = document.getElementById("wait");


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


// handle form submission 
formElt.addEventListener("submit", function(e) {
    console.log("Formulaire validé");
    e.preventDefault()
    let searchText = "";
    searchText = formElt.elements.search.value;
    console.log("La valeur reçue: ", searchText);

    addTextToChat(searchText, 'visitorClasses');

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
                console.log("Try again: ", response.statusText);
                waitElt.classList.toggle("invisible");
                throw error
            }
        })
        .then((answer) => {
            console.log("On passe à la création des phrases réponses.")
            waitElt.classList.toggle("invisible");

            if (answer['error']) {
                throw error;
            }
            
            if (answer['greetings']) {
                robotCommunicates('greetings', answer['greeting_word']);
            }

            robotCommunicates('intro');

            if (answer['rephrase']) {
                return robotCommunicates('rephrase');
            }

            if (answer['notsure']) {
                tellMoreAbout(answer, false);

                let mapElt = createMap(answer['gmaps'].coord);
                addMapToChat(mapElt);

                return
            }
            
            robotCommunicates('sure', answer['look_for'])

            let direction;
            direction = "L'adresse pour t'y rendre c'est: " + answer['gmaps'].address;
            robotCommunicates('direct', direction)

            let mapElt = createMap(answer['gmaps'].coord);         
            addMapToChat(mapElt);
            
            // delay before displaying more informations
            setTimeout(tellMoreAbout, 3000, answer);

        })
        .catch((error) => {
            robotCommunicates('error')
            console.error("Quelque chose s'est mal passé: ", error);
        })
        .finally(() => {
            formElt.elements.search.value="";
        });
});
