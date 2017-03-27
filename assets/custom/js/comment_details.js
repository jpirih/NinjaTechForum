/**
 * Created by janko on 26/03/2017.
 * This js file is for manipulating with  comment details modal - edit and delete
 */

$(document).ready(function () {

    console.log("comment details js is ready!");
    var commentContent = $(".comment-content");
    var editCommentBtn = $(".edit");
    var editCommentForm = $(".edit-comment-form");

    editCommentForm.hide();
    editCommentBtn.click(function() {
        commentContent.toggle(this.id);
        editCommentForm.toggle(this.id);
    });
});
