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

}

// collection of hesitating sentences
const hesitating = {
    0: "J'hésite... "
}

// create <li> element to be added
const createListElt = (content, classTags) => {
    let liElt = document.createElement("li");
    let tagsList = customTags[classTags];

    liElt.classList.add(...tagsList);
    liElt.textContent = content;
    return liElt;
}

// insert dialog elements to the chat
const addTextToChat = (content, classTags) => {
    let liElt = createListElt(content, classTags);
    questionListElt.insertAdjacentElement("afterbegin", liElt);
}

// insert links elements to the chat
const addLinkToChat = (link, classTags) => {
    
    let linkElt = document.createElement("a");
    linkElt.href = link;
    linkElt.target = '_blank';
    linkElt.textContent = "Si tu veux en savoir encore plus..."

    let tagsList = customTags[classTags];
    linkElt.classList.add(...tagsList);
    
    questionListElt.insertAdjacentElement("afterbegin", linkElt);
}

// insert map element to the chat
const addMapToChat = (content) => {
    console.log("Ajout de la carte à la conversation.");
    questionListElt.insertAdjacentElement("afterbegin", content);
}

// add complementary informations to the chat
const tellMeMoreAbout = (source) => {
    const text = source['wikipedia'].extract;
    const link = source['wikipedia'].url;

    // choose a random sentence opening
    let message = boasting[Math.floor(Math.random()*3)] + text

    addTextToChat(message, 'robotClasses');
    addLinkToChat(link, 'robotClasses');
}


export { addMapToChat, addTextToChat, tellMeMoreAbout}