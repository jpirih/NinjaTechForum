/**
 * Created by janko on 25/03/2017.
 */
var topicEditForm = $("#edit-form");

$(document).ready(function () {
   console.log("We are ready let's go!");
   var topicTitle = $("#topic-main-title").html();
   var topicMainTitle = $("#topic-main-title")
   var editBtn = $("#edit-button");
   var topicContent = $("#topic-content");


   editBtn.click(function () {
       // toggling between content and edit form
       topicContent.toggle();
       topicEditForm.toggle();
       // button text changing
       if(topicEditForm.is(":hidden") === true){
           topicMainTitle = topicMainTitle.html(topicTitle);
           editBtn.html("Edit")

       }else{
           var topicEditTitle = "Edit topic "+ topicTitle;
           topicMainTitle = topicMainTitle.html(topicEditTitle);
           editBtn.html("Show Content")
       }


   });




});
