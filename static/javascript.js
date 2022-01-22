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

    myTester()
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

function sendToPythonAndWait(text)
{
    return new Promise((resolve, reject) =>
    {
        sendToPython(text);
        socket.on('message_from_python', function(msg) {
            resolve(msg);
        })
    });
}

async function myTester() {
    console.log("myTester called")

    {
        const response = await sendToPythonAndWait("book a single ticket friday 10pm from northampton to london");
        if (response === "------------------------FOR 28/01/22-----------------------<br> The cheapest journey departs from Northampton</mark> at 22:07, and arrives at London Euston at 23:30.<br>The journey will take 1 hour  and 23 minutes, and has 0 changes.<br>The ticket will cost £9.50.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/northampton/london/280122/2200/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by London Northwestern Railway)<br>") {
            console.log("Test 1 Passed")
        } else {
            console.log("Error: Unexpected Response:\n" + msg + "\n")
        }
    }

    {
        const response = await sendToPythonAndWait("book a single ticket friday 10pm from london to northampton");
        if (response === "------------------------FOR 28/01/22-----------------------<br> The cheapest journey departs from London Euston</mark> at 22:18, and arrives at Northampton at 23:48.<br>The journey will take 1 hour  and 30 minutes, and has 0 changes.<br>The ticket will cost £9.50.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/london/northampton/280122/2200/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by London Northwestern Railway)<br>") {
            console.log("Test 2 Passed");
        } else {
            console.log("Error: Unexpected Response:\n" + msg + "\n")
        }
    }

    {
        // TESTING VALID GREETING INPUTS, CREATE SEPARATE TESTS FOR INVALID (unable_to_parse) INPUTS
        /*      helloRegex = [
        {"LOWER": {"REGEX": "hi(?![\S])|hey(?![\S])|yo(?![\S])|hello(?![\S])"}}*/

        const listsOfResponses = [
            ["Hello there! What assistance do you need?", "Hi there! How can I help?", "Nice to see you! What can I do for you?", "Hello, can i help?", "Hi! Is there anything you would like my help with?"],
            ["Will this be a single, or a return ticket?"]
            //add more response lists here
        ]

        const listsofInputs = [
            ["hi", "hey", "yo", "hello", "hello my name is Bob", "Hi I need some help", "this should fail"],
            ["booking", "book", "ticket", "buy", "i'd like to book a ticket please"]
            //add more input lists for the corresponding response list in listsOfResponses
        ]


        for (let list = 0; list < listsofInputs.length; list++) {
            for (let input = 0; input < listsofInputs[list].length; input++) {
                let success = false
                const actualResponse = await sendToPythonAndWait(listsofInputs[list][input]);
                //console.log("list=" + list + " input=" +input)
                //console.log("current input: " +listsofInputs[list][input])
                for (let response = 0; response < listsOfResponses[list].length; response++ ) {
                    //console.log("listsofResponses[" + list + "][" + response + "]")
                    //console.log("comparison response: " + listsofResponses[list][response])
                    //console.log("actual response: "+actualResponse)
                    if (actualResponse === listsOfResponses[list][response]) {
                        //console.log("Test " + list + "." + input + " Passed with User Input: \"" + listsofInputs[list][input] + "\" and Bot Response: \"" + actualResponse + "\".")
                        success = true
                    }
                }

                if (success === true) {
                    console.log("Test " + list + "." + input + " Passed with User Input: \"" + listsofInputs[list][input] + "\" and Bot Response: \"" + actualResponse + "\".")
                } else {
                    console.log("ERROR: Test " + list + "." + input + " Failed with User Input:  \"" + listsofInputs[list][input] + "\" and Bot Response: \"" + actualResponse + "\".")
                }
            }
        }

    }

    //{
/*        const helloGreeting = ["hi", "hey", "yo", "hello", "hello my name is Bob", "Hi I need some help"]

        for (let i in helloGreeting) {
            const response = await sendToPythonAndWait(helloGreeting[i]);

            //console.log(response)

            if (response === "Hello there! What assistance do you need?" || response === "Hi there! How can I help?" || response === "Nice to see you! What can I do for you?" || response === "Hello, can i help?" || response === "Hi! Is there anything you would like my help with?") {
                console.log("Test 3."+ i + " Passed with User Input: \"" + helloGreeting[i] + "\" and Bot Response: \"" + response + "\".")
            }
            else {
                console.log("ERROR: Test 3." + i + " Failed with User Input:  \"" + helloGreeting[i] + "\" and Bot Response: \"" + response + "\".")
                // console.log("Error: Unexpected Response:\n" + response + "\n")
            }
            i++
        }*/
    //}
}





