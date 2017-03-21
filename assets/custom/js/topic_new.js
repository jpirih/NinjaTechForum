/**
 * Created by janko on 20/03/2017.
 */

$(document).ready(function () {
            console.log("Test delovanja - pripravljeni ");


            // variables
            var mainTitle = $("#main-title");
            var topicButton = $("#topic-button");
            var setTitle = $("#title");

            var robot_test = $("#robot-test");
            var label_robot_test = $("#robot-test-label");
            var num1 = Math.floor((Math.random() * 10) + 1);
            var num2 = Math.floor((Math.random() * 10) + 1);
            var result = num1 + num2;

            label_robot_test.text("Enter sum of " + num1 + " and " + num2);


            topicButton.attr("disabled", true);

            // robot test function
            robot_test.on("keyup", function () {
                setTimeout(function () {

                    var user_value = parseInt(robot_test.val());
                    if(user_value === result) {
                        topicButton.removeAttr("disabled");

                        }else {
                        topicButton.attr("disabled", true);
                    }
                    }, 1000)
            });

            // jquery simplistic tasks
            topicButton.removeClass("btn-success");
            topicButton.addClass("btn-danger");
            mainTitle .css("font-size", "2.5 em ");

            setTitle.attr("placeholder", "Add topic title");

            topicButton.click(function () {
                console.log("Click! :)");
                topicButton.hide();
            });

            // show main title - for fun
            mainTitle.hide();
            function showTitle() {
                setTimeout(function () {
                      mainTitle.show();
                }, 2000)
            }

            showTitle();

        });
