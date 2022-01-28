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

    testHarness()        //call test harness
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

// Tester class called from javascript.js

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



async function testHarness() {

    console.log("testHarness called")

    const listsOfResponses = [
        ["Hello there! What assistance do you need?", "Hi there! How can I help?", "Nice to see you! What can I do for you?", "Hello, can i help?", "Hi! Is there anything you would like my help with?"],
        ["Happy to help!", "Happy to be of assistance!", "Glad I could help!", "My pleasure!"],
        ["Bye! See you again soon!", "Farewell!", "Until next time!"],
        ["Hi! What would you like me to do? I can either help you make a booking, or find potential delays.", "Hi there! Would you like me to help find potential delays, or assist with a booking?"],
        ["I didn't quite understand that. Sorry!", "Oops, I don't quite understand.", "Apologies, but I didn't understand that."],
        ["Will this be a single, or a return ticket?"],
        ["Where would you like to depart from?", "Where will you be departing from?"],
        ["Where would you like to travel to?", "Where will you be travelling to?"],
        ["Please specify a time for this outbound journey."],
        ["And please specify a time for your return journey."],
        ["What date do you want to depart on?", "What date will you be leaving on?"],       //#10
        ["What date would you like to return on?", "Which date will you be coming back on?"],
        ["Sorry! I don't quite understand that date! Please input it again."],
        ["Sorry, that date is in the past! Please request another date.", "I'm afraid that date is in the past, oops! Please specify another date."],
        ["Sorry, that date is too far in the future for the National Rail website to support! Please enter a closer date."],
        ["Oops! I didnt quite understand that time. Can you repeat it in a HH:MM format?"],
        ["Sorry, that time is in the past! Please request another time.", "I'm afraid that time is in the past, oops! Please specify another time."],
        ["My apologies, we could not find any results for this journey.", "Sorry, there are no tickets available for this journey"],
        ["Sorry, that return date is before your departure date! Please enter your return date again."],
        ["Do you want to book another ticket or see potential train delays?", "Now, do you want to book a different ticket or see potential train delays?"],
        ["What station did you depart from?"],
        ["What station are you going to?"],
        ["What station are you currently at?"],
        ["How long is your quoted delay time, in minutes?"],
        ["Sorry, I can only predict a delay if I am given a valid station! Please specify again."],
        ["Sorry, you cannot choose this station! Please specify again."],
        ["Apologies, I could not quite understand that time! Please state it again."],
        ["What time did you depart?"],

        // Error handling messages
        ["Sorry, the destination and departure locations cannot be the same!"],
        // Thrown from getData in getTicketData
        ["Sorry, I didnt understand that query! Would you like me to help you make a booking, or find potential delays?"],
        //
        ["Oops! I couldn't find any results for that journey, please try again." + " I can help you book a train ticket, or predict delays, what would you like me to do?"],

        //predictDelay responses
        ["Getting train data..."],
        ["Sorry, I cant find any train IDs for that route. " +
        "Want me to predict another route, or book a train ticket?"],
        ["Sorry, it doesn't seem like this route was valid. " +
        "Want me to predict another route, or book a train ticket?"],
        ["Predicting delay..."],
        ["Good news! You are still expected to arrive on time. Thanks for using our service."],
        ["I predict that you will be just 1 minute late to your destination. Thanks for using our service."],
        //["I predict that you will be " + str(                                                                         //requires explicit final output response
        //                     prediction) + " minutes late to your destination. Thanks for using our service."]
        ["Sorry, I can't find the station you're at on this route. Want me to predict another delay, or book a train ticket?"],
        ["Sorry, I couldn't find any results for this journey. Want me to predict another route, or book a train ticket?"]

    ]

    // STEP 1: Specify input strings inside a new nested list
    const listsOfInputs = [
        ["booking", "single", "cambridge", "norwich", "today", "8:00"],
        ["book", "single", "London", "Norwich", "tomorrow", "noon"],
        ["book a single ticket", "northampton", "london", "friday#", "12pm"],
        ["hello i would like to book a train ticket", "single please", "cambridge", "london liverpool street", "25th feb", "i want to arrive before 4pm"],
        // testing all different date and time formats //
        ["booking", "single", "cambridge", "norwich", "monday", "1:45pm"],
        ["booking", "single", "cambridge", "norwich", "tuesday", "1:45 p.m."],
        ["booking", "single", "cambridge", "norwich", "23/02/22", "morning"],
        ["booking", "single", "cambridge", "norwich", "23/02/2022", "noon"],
        ["booking", "single", "cambridge", "norwich", "23/02", "afternoon"],
        ["booking", "single", "cambridge", "norwich", "23rd feb", "midnight"],
        ["booking", "single", "cambridge", "norwich", "23rd february", "whenever"],
        ["booking", "single", "cambridge", "norwich", "23rd feb 2022", "i want to arrive before 4pm"],
        ["booking", "single", "cambridge", "norwich", "23rd of february", "i want to leave before 10:45"],
        ["booking", "single", "cambridge", "norwich", "23rd february 2022", "13:45"],
        ["booking", "single", "cambridge", "norwich", "23rd of feb", "13:45"],
        // testing other input formats //
        ["I want a single train ticket from norwich to london", "23rd of feb", "13:45"],
        ["single ticket from IPS to LST", "23rd of feb", "13:45"],
        ["book me a return ticket", "cambridge", "norwich", "23rd of feb", "13:45", "25th of feb", "12:00pm"],
        //predict delay
        ["I am delayed", "norwich", "london liverpool street", "ipswich", "10am", "10"]

    ]

    // STEP 2: add a new string for that expected final output (all correct as of 28/01/22 - inputs with strings such as "today" will produce different outputs depending on when they are run)
    const finalExpectedOutputStringList = [
        "------------------------FOR 28/01/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 09:00, and arrives at Norwich at 10:14.<br>The journey will take 1 hour  and 14 minutes, and has 1 change.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/280122/0800/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>",
        "------------------------FOR 29/01/22-----------------------<br> The cheapest journey departs from London Liverpool Street</mark> at 12:18, and arrives at Norwich at 14:46.<br>The journey will take 2 hours  and 28 minutes, and has 2 changes.<br>The ticket will cost £18.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/London/NRW/290122/1200/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(Some or all of this journey is via bus. Check the booking website for details)<br>",
        "------------------------FOR 04/02/22-----------------------<br> The cheapest journey departs from Northampton</mark> at 12:05, and arrives at London Euston at 13:23.<br>The journey will take 1 hour  and 18 minutes, and has 0 changes.<br>The ticket will cost £9.50.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/northampton/london/040222/1200/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by London Northwestern Railway)<br>",
        "------------------------FOR 25/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 14:03, and arrives at London Liverpool Street at 15:15.<br>The journey will take 1 hour  and 12 minutes, and has 0 changes.<br>The ticket will cost £8.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/london liverpool street/250222/1600/arr\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        // testing all different date and time formats //
        "------------------------FOR 31/01/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 14:20, and arrives at Norwich at 15:40.<br>The journey will take 1 hour  and 20 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/310122/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>",
        "------------------------FOR 01/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 14:20, and arrives at Norwich at 15:40.<br>The journey will take 1 hour  and 20 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/010222/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 09:00, and arrives at Norwich at 10:14.<br>The journey will take 1 hour  and 14 minutes, and has 1 change.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/0900/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 12:20, and arrives at Norwich at 13:39.<br>The journey will take 1 hour  and 19 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1200/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 13:20, and arrives at Norwich at 14:42.<br>The journey will take 1 hour  and 22 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1300/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 06:02, and arrives at Norwich at 07:25.<br>The journey will take 1 hour  and 23 minutes, and has 0 changes.<br>The ticket will cost £29.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/0000/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 20:20, and arrives at Norwich at 21:37.<br>The journey will take 1 hour  and 17 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/2000/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 12:20, and arrives at Norwich at 13:39.<br>The journey will take 1 hour  and 19 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1600/arr\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 06:02, and arrives at Norwich at 07:25.<br>The journey will take 1 hour  and 23 minutes, and has 0 changes.<br>The ticket will cost £29.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1045/first\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 14:20, and arrives at Norwich at 15:40.<br>The journey will take 1 hour  and 20 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Cambridge</mark> at 14:20, and arrives at Norwich at 15:40.<br>The journey will take 1 hour  and 20 minutes, and has 0 changes.<br>The ticket will cost £20.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        // testing other input formats //
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Norwich</mark> at 14:01, and arrives at London Liverpool Street at 15:51.<br>The journey will take 1 hour  and 50 minutes, and has 0 changes.<br>The ticket will cost £10.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/norwich/london/230222/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest journey departs from Ipswich</mark> at 13:41, and arrives at London Liverpool Street at 14:51.<br>The journey will take 1 hour  and 10 minutes, and has 0 changes.<br>The ticket will cost £10.00.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/ips/lst/230222/1345/dep\" target=\"_blank\"> click here.</a> <br> (Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details)",
        "------------------------FOR 23/02/22-----------------------<br> The cheapest outbound journey departs from Cambridge at 14:20, and arrives at Norwich at 15:40.<br> This journey will take 1 hour  and 20 minutes, and has 0 changes.<br>(Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details.) <br>------------------------FOR 25/02/22-----------------------<br> The cheapest inbound journey departs from Norwich at 11:56, and arrives at Cambridge at 13:12.<br>This journey will take 1 hour  and 16 minutes, and has 1 change.<br>(Journey provided by Greater Anglia)<br>(There may be some disruption on this route. Check the booking website for details.) <br><br> This return ticket will cost £26.50.<br> To view your booking, <a href=\"https://ojp.nationalrail.co.uk/service/timesandfares/cambridge/norwich/230222/1345/dep/250222/1200/dep\" target=\"_blank\"> click here.</a> <br> ",
        //predictdelay
        "Getting train data...."
    ]

    // STEP 3: Specify the appropriate category of response for each input string (category = the index in listsOfResponses)
    const listsOfExpectedResponseCategories = [
        [5,6,7,10,8],
        [5,6,7,10,8],
        [6,7,10,8],
        [5,6,7,10,8],
        // testing all different date and time formats //
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        [5,6,7,10,8],
        // testing other input formats //
        [10,9],
        [10,9],
        [6,7,10,8,11,9],
        //error handling
        [5,6,7,8,8,8],
        //predictdelay
        [20,21,22,27,23]
    ]

    //function to compare returned category list with expected category list
    const equals = (a, b) => JSON.stringify(a) === JSON.stringify(b);

    //run tests
    for (let list = 0; list < listsOfInputs.length; list++) {
        let responseTypeList = []
        for (let input = 0; input < listsOfInputs[list].length; input++) {
            let success = false
            const actualResponse = await sendToPythonAndWait(listsOfInputs[list][input]);

            if (input === listsOfInputs[list].length - 1) {       // if last input in the current input list
                if (actualResponse === finalExpectedOutputStringList[list]) {

                    console.log("Intermediate Test " + list + "." + input + " Passed with User Input: \"" + listsOfInputs[list][input] + "\" and Bot Final Response: \"" + actualResponse + ".")
                    const equal = equals(responseTypeList, listsOfExpectedResponseCategories[list])

                    if (equal) {
                        console.log("\nFull Test " + list + " Passed with: \nUser Input: \"" + listsOfInputs[list] + "\nResponse Categories: " + responseTypeList + "\nFinal Response: " + actualResponse + ".\n\n")
                    }
                    success = true
                    break;
                } else {
                    console.log("\nERROR: Full Test " + list + " Failed with User Input:  \"" + listsOfInputs[list][input] + "\" and Bot Final Response: \"" + actualResponse + ".\n\n")
                    break;
                }
            }

            for (let responseList = 0; responseList < listsOfResponses.length; responseList++) {        //loop through each possible response
                for (let response = 0; response < listsOfResponses[responseList].length; response++) {
                    if (actualResponse === listsOfResponses[responseList][response]) {
                        console.log("Intermediate Test " + list + "." + input + " Passed with User Input: \"" + listsOfInputs[list][input] + "\" and Bot Response: \"" + actualResponse + "\" of type: " + responseList + ".")
                        responseTypeList.push(responseList);
                        success = true
                        break;
                    }
                }
                if (success === true) {
                    break;
                }
            }
            if (!success) {
                console.log("ERROR: Intermediate Test " + list + "." + input + " Failed with User Input:  \"" + listsOfInputs[list][input] + "\" and Bot Response: \"" + actualResponse + "\".")
                console.log("ResponseTypeList: " + responseTypeList)
            }
        }
    }
}







