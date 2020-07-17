const questionListElt = document.getElementById("chat");

// collection of classes tags for dialogue
const customTags = {
    'visitorClasses': ["visitor", "shadow", "my-md-2", "list-group-item", "list-group-item-warning"],
    'robotClasses': ["robot", "shadow", "my-md-2", "text-right", "list-group-item", "list-group-item-success"],
    'robotAlertClasses': ["robot", "shadow", "my-md-2", "text-right", "list-group-item", "list-group-item-danger"]
};

// collection of add-on sentences
const boasting = {
    0: "D'ailleurs puisque tu insistes pour que je t'en dise plus... ",
    1: "A ce propos... ",
    2: "Savais tu que... "
};

// collection of condifent sentences
const confident = {
    0: "Je connais très bien ",
    1: "Excellent choix ",
    2: "Haaaa "
};

// collection of hesitating sentences
const hesitating = {
    0: "J'hésite sur ta demande... ",
    1: "Je ne suis pas bien sûr d'avoir compris la demande. ",
    2: "Je n'ai peut être pas bien compris ta demande. "
};

// collection of introduction sentences
const introduction = {
    0: "Voyons voir... ",
    1: "Laisse moi y réfléchir... ",
    2: "Ha ! une question ! "
};

// create <li> element to be added
const createListElt = (content, classTags) => {
    let liElt = document.createElement("li");
    let tagsList = customTags[classTags];

    liElt.classList.add(...tagsList);
    liElt.textContent = content;
    return liElt;
};

// insert dialog elements to the chat
const addTextToChat = (content, classTags) => {
    let liElt = createListElt(content, classTags);
    questionListElt.insertAdjacentElement("afterbegin", liElt);
};

// insert links elements to the chat
const addLinkToChat = (link, classTags) => {
    
    let linkElt = document.createElement("a");
    linkElt.href = link;
    linkElt.target = '_blank';
    linkElt.textContent = "Si tu veux en savoir encore plus..."

    let tagsList = customTags[classTags];
    linkElt.classList.add(...tagsList);
    
    questionListElt.insertAdjacentElement("afterbegin", linkElt);
};

// insert map element to the chat
const addMapToChat = (content) => {
    console.log("Ajout de la carte à la conversation.");
    questionListElt.insertAdjacentElement("afterbegin", content);
};

// add complementary informations to the chat
const tellMoreAbout = (source, sure=true) => {
    const text = source['wikipedia'].extract;
    const link = source['wikipedia'].url;

    robotCommunicates(sure ? 'boast' : 'notsure', text);
    addLinkToChat(link, 'robotClasses');
};


// choose a random sentence opening any communication of the robot
const robotCommunicates = (type, complementaryText='') => {
    let sentence = '';
    switch (type) {

        case 'direct':
            break;

        case 'greetings':
            sentence = complementaryText + " !"
            return addTextToChat(sentence, 'robotClasses');

        case 'intro':
            sentence = introduction[Math.floor(Math.random() * 3)] + "\n";
            break;

        case 'notsure':
            sentence = hesitating[Math.floor(Math.random() * 3)] + "\n";
            sentence += "Ce que je peux te dire en revanche c'est que ";
            break;
        
        case 'sure':
            sentence = confident[Math.floor(Math.random() * 3)];
            break;

        case 'boast':
            sentence = boasting[Math.floor(Math.random() * 3)];
            break;

        case 'rephrase':
            sentence = "Désolé, je n'ai pas compris ta demande... \n Pourrais-tu la reformuler autrement ? \n";
            return addTextToChat(sentence, 'robotAlertClasses');

        case 'error':
            sentence = "Je suis désolé, mais ma réflexion n'a pas abouti... Peux tu reformuler ta demande ? \n";
            return addTextToChat(sentence, 'robotAlertClasses');
        
        default:
            throw 'Mauvais paramètre pour la fonction robotCommunicates'; 
    }
    sentence += complementaryText;
    return addTextToChat(sentence, 'robotClasses');
};


export { addMapToChat, addTextToChat, tellMoreAbout, robotCommunicates}