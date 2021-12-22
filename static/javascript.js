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

    document.getElementById("chatBox").appendChild(chatGroup)
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
    document.getElementById("chatBox").appendChild(chatGroup)

}

window.onload = function () {
 setTimeout(function () {
 addRobotMessage("whats 9+10");
},1000)

 setTimeout(function () {
 addHumanMessage("21");
},2000)

 setTimeout(function () {
 addRobotMessage("ur train is fucking late");
},3000)

 setTimeout(function () {
 addHumanMessage("can i book another one");
},4000)


 setTimeout(function () {
 addRobotMessage("go fuck yourself");
},5000)

     setTimeout(function () {
 addHumanMessage("okay the scrolling works this can stop now");
},6000)


};
