let micRunning = false;
let volume = 0;

    //This adds a robot message. Look at the commented HTML in the HTML file for the format and structure that is
    //being mimicked here
function addRobotMessage(text) {
    speech(text);
    const chatGroup = document.createElement("div");
    chatGroup.className = "chatGroup robot"
    const avatar = document.createElement("div");
    avatar.className = "avatar"
    const avatarFigure = document.createElement("figure");
    const avatarPNG = document.createElement("img");
    avatarPNG.src = "/static/robot_small.png"
    avatarFigure.appendChild(avatarPNG)
    avatar.appendChild(avatarFigure)
    chatGroup.appendChild(avatar)
    const actualText = document.createElement("div");
    actualText.className = "actualText"
    chatGroup.appendChild(actualText)
    const bubble = document.createElement("div");
    bubble.className = "bubble"
    bubble.innerHTML = text
    actualText.appendChild(bubble)
    const time = document.createElement("div");
    time.className = "time"
    time.innerHTML = getTime();
    actualText.appendChild(time)
    const chatBox = document.getElementById("chatBox");
    chatBox.appendChild(chatGroup)
    chatBox.scrollTop = chatBox.scrollHeight
}
    //Similar to the above function but this adds a human message to the conversation
function addHumanMessage(text) {
    const chatGroup = document.createElement("div");
    chatGroup.className = "chatGroup human";
    const actualText = document.createElement("div");
    actualText.className = "actualText";
    chatGroup.appendChild(actualText)
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = text;
    actualText.appendChild(bubble);
    const time = document.createElement("div");
    time.className = "time"
    time.innerHTML = getTime();
    actualText.appendChild(time)
    const chatBox = document.getElementById("chatBox");
    chatBox.appendChild(chatGroup);
    chatBox.scrollTop = chatBox.scrollHeight;

}
    //When send button is pressed, and there is text in the text box, make it a message and send the text to Python
function onSendPressed() {
    const textBoxInput = document.getElementById('textBoxInput');
    if (textBoxInput.value !== "") {
        removeTextGlow();
        addHumanMessage(textBoxInput.value);
        sendToPython(textBoxInput.value);
        textBoxInput.value = "";
    }
}
    //This is the speech recognition function. Some extra CSS and UI tweaks are changed while/after recognition.
    //The resulting text is injected into the message box.
function micAnalysis() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.onstart = () => {
        document.getElementById('micIcon').src = "/static/recording.gif";
        document.getElementById('textBoxInput').style.width = '592px';
        micRunning = true;
        removeTextGlow();
    }
    recognition.onend = () => {
        document.getElementById('micIcon').src = "/static/mic.png";
        document.getElementById('textBoxInput').style.width = '602px';
        micRunning = false;
        document.getElementById('sendButton').focus();
    }

    recognition.onresult = (event) => {
        speechText = event.results[0][0].transcript;
        if (speechText.length > 1) {
            const textBoxInput = document.getElementById('textBoxInput');
            textBoxInput.value = speechText;
            textBoxInput.classList.add('animate');
        }
    }

    document.getElementById('micButton').onclick = () => {
        if (micRunning === false) {
            recognition.start();
        }
        else {
            recognition.stop();
        }
    }
}
    //Removing the CSS from the above function when the user sends the message or clicks in a certain area
function removeTextGlow() {

    const textBoxInput = document.getElementById('textBoxInput');
    if (textBoxInput.classList.contains('animate')) {
        textBoxInput.classList.remove('animate');
    }

}
    //This is the text-to-speech function. The regex means it will not say what it matches, which is used to
    //just format a ticket message. Otherwise, it will say everything else when the sound icon is clicked
function speech(text) {
    var newText = text.replace(/------------------------FOR \d\d\/\d\d\/\d\d-----------------------/g, "")
    var synth = window.speechSynthesis;
    var utter = new SpeechSynthesisUtterance(newText);
    utter.volume = volume;
    synth.speak(utter);
}
    //This gets the current time to be appended beneath each message
function getTime() {
    const date = new Date();
    const hours = (date.getHours() < 10 ? '0' : '') + date.getHours();
    const minutes = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes();

    return hours + ":" + minutes;
}
    //This toggles the text-to-speech
function volumeButtonClicked() {
    const volumeIcon = document.getElementById('volumeIcon');
    if (volume === 0) {
        volumeIcon.src = "/static/volume_on.png";
        volume = 1;
    }
    else {
        volumeIcon.src = "/static/volume_off.png";
        volume = 0;
        speechSynthesis.cancel()
    }

}


