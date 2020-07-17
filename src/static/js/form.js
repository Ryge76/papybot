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

    //TODO: ajouter une phrase random
    // addTextToChat("Laisse moi y réfléchir...", 'robotClasses');
    // robotCommunicates('intro');
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
                waitElt.classList.toggle("invisible");
                throw error
            }
        })
        .then((answer) => {
            console.log("On passe à la création des phrases réponses.")
            waitElt.classList.toggle("invisible");

            // let sentence = "";
            
            //TODO: case 'error' in answer
            if (answer['error']) {
                throw error;
            }
            
            if (answer['greetings']) {
                // sentence = answer['greeting_word'] + " !\n";
                robotCommunicates('greetings', answer['greeting_word']);
            }

            robotCommunicates('intro');

            if (answer['rephrase']) {
                // sentence += "Désolé, je n'ai pas compris ta demande... \n Pourrais-tu la reformuler autrement ? \n";
                // return addTextToChat(sentence, 'robotAlertClasses');
                return robotCommunicates('rephrase');
            }

            if (answer['notsure']) {
                // TODO: function to generate various hesitation expressions
                // let complement = "Ce que je sais c'est que " + answer['wikipedia'].extract;
                // sentence += "\n Si tu veux en savoir plus: " + answer['wikipedia'].url;
                
                // robotCommunicates('notsure', complement);
                // robotCommunicates('direct', );

                tellMoreAbout(answer, false);

                let mapElt = createMap(answer['gmaps'].coord);
                addMapToChat(mapElt);

                // addTextToChat(sentence, 'robotClasses');
                return
            }


            // TODO: function to generate various ok response + refactoring of display maps
            // sentence += "Je connais bien " + answer['look_for'] + ". \n";
            // sentence += "L'adresse pour t'y rendre c'est: " + answer['gmaps'].address;
            
            robotCommunicates('sure', answer['look_for'])

            let direction;
            direction = "L'adresse pour t'y rendre c'est: " + answer['gmaps'].address;
            robotCommunicates('direct', direction)

            let mapElt = createMap(answer['gmaps'].coord);         
            addMapToChat(mapElt);
            // addTextToChat(sentence, 'robotClasses');

            // delay before displaying more informations
            setTimeout(tellMoreAbout, 3000, answer);

        })
        .catch((error) => {
            // addTextToChat("Je suis désolé, mais ma réflexion n'a pas abouti... Peux tu reformuler ta demande ?", 'robotAlertClasses');
            robotCommunicates('error')
            console.error("Quelque chose s'est mal passé: ", error);
        })
        .finally(() => {
            formElt.elements.search.value="";
        });
});
