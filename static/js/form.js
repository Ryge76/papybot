const formElt = $("#query");
const questionListElt = $(".test li:first");
console.log("je suis form.js !")

formElt.change((e)=>{
    console.error('Je suis bien appelé !')
    let queryText = "";
    queryText = $(this).text();
    questionListElt.insertBefore(queryText);
})


