var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

function addRobotMessage(text) {
    var chatGroup = document.createElement("div")
    chatGroup.className = "chatGroup robot"
        var avatar = document.createElement("div")
        avatar.className = "avatar"
            var avatarFigure = document.createElement("figure")
                var avatarPNG = document.createElement("img")
                avatarPNG.src = "/static/robot_small.png"
            avatarFigure.appendChild(avatarPNG)
        avatar.appendChild(avatarFigure)
    chatGroup.appendChild(avatar)
        var actualText = document.createElement("div")
        actualText.className = "actualText"
    chatGroup.appendChild(actualText)
            var bubble = document.createElement("div")
            bubble.className = "bubble"
            bubble.innerHTML = text
        actualText.appendChild(bubble)
            var time = document.createElement("div")
            time.className = "time"
            time.innerHTML = "12:25" /* CHANGE THIS TO ACTUAL TIME */
         actualText.appendChild(time)
    var chatBox = document.getElementById("chatBox")
    chatBox.appendChild(chatGroup)
    chatBox.scrollTop = chatBox.scrollHeight
}

function addHumanMessage(text) {
    var chatGroup = document.createElement("div")
    chatGroup.className = "chatGroup human"
        var actualText = document.createElement("div")
        actualText.className = "actualText"
    chatGroup.appendChild(actualText)
            var bubble = document.createElement("div")
            bubble.className = "bubble"
            bubble.innerHTML = text
        actualText.appendChild(bubble)
            var time = document.createElement("div")
            time.className = "time"
            time.innerHTML = "12:25" /* change this to actual time, use 24h */
        actualText.appendChild(time)
    var chatBox = document.getElementById("chatBox")
    chatBox.appendChild(chatGroup)
    chatBox.scrollTop = chatBox.scrollHeight

}

function onSendPressed() {
    var textBoxInput = document.getElementById('textBoxInput')
    $.ajax({
                type: "POST",
                url: "/post",
                contentType: "application/json",
                data: JSON.stringify({text: textBoxInput.value}),
                dataType: "json",
                success: function(response) {
                    addRobotMessage(response['responseText']);
                },
                    //extremely bad practice
                error: function(err) {
                    addRobotMessage(err['responseText']);
                    console.log(err)
                }
            });
    if (textBoxInput.value !== "") {
        addHumanMessage(textBoxInput.value)
        textBoxInput.value = ""
    }
}