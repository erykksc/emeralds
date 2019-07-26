var url = window.location.href;
url=url.slice(7,-1)
url = "ws://" + url + "/socketserver";

var socket = new WebSocket(url);

socket.onopen= function(event)
{
    renderEnterNickname();
}

socket.onmessage = function (event)
{
    message = event.data;
    console.log(message);

    //messages about usernames
    if (message=="USERNAME OK")
    {
        renderPressToContinute();
    }
    else if (message=="USERNAME TAKEN")
    {
        alert("Username has already been taken");
    }
    else if (message=="USERNAME NOT_ACCEPTING")
    {
        alert("Server is not accepting new users");
    }

    else if (message=="DECISION OK")
    {
        renderWaiting();
    }
    else if (message=="DECISION NOT_ACCEPTING")
    {
        alert("Server is not accepting decisions");
    }

    else if (message=="RENDER WAITING")
    {
        renderWaiting();
    }
    else if (message=="RENDER DECISION")
    {
        renderDecision();
    }
    else if (message=="RENDER ENTER_NICKNAMES")
    {
        renderEnterNickname();
    }
    else if (message=="RENDER PRESS_TO_CONTINUE")
    {
        renderPressToContinute();
    }
}


function sendDecision(explores)
{
    socket.send("d " + String(explores))
}

function sendUsername()
{
    var usernameDOM = document.getElementById("username");
    var username = String(usernameDOM.value).trim();
    if (username===""){ return false;}
    socket.send("n " + username);
    waitForUsernameAccept=true
}

function renderEnterNickname()
{
    document.body.innerHTML=""

    var h1 = document.createElement("h1");
    h1.textContent="Emeralds";
    document.body.appendChild(h1);

    var username = document.createElement("input");
    username.type = "text"
    username.id = "username";
    username.placeholder = "Username";
    username.maxLength = 20;
    username.autofocus=true;
    document.body.appendChild(username);

    var breakln = document.createElement("br")
    document.body.appendChild(breakln)
    var breakln = document.createElement("br")
    document.body.appendChild(breakln)

    var submitBtn = document.createElement("input")
    submitBtn.id = "sendUsername_button";
    submitBtn.type="button";
    submitBtn.value = "Send Username";
    document.body.appendChild(submitBtn);

    document.getElementById('sendUsername_button').addEventListener("click", sendUsername);
}

function renderDecision()
{
    document.body.innerHTML=""

    var h1 = document.createElement("h1");
    h1.textContent="Emeralds";
    document.body.appendChild(h1);

    var gemsInChest = document.createElement("p")
    gemsInChest.id = "gemsInChest";
    gemsInChest.textContent="Gems in chest: 0";
    document.body.appendChild(gemsInChest);

    var unsavedGems = document.createElement("p")
    unsavedGems.id = "unsavedGems";
    unsavedGems.textContent="Unsaved gems: 0";
    document.body.appendChild(unsavedGems);

    var explore_button = document.createElement("input")
    explore_button.id = "explore_button";
    explore_button.type="button";
    explore_button.value = "Explore";
    document.body.appendChild(explore_button);

    document.getElementById("explore_button").addEventListener("click", function(){sendDecision(true);});

    var breakln = document.createElement("br")
    document.body.appendChild(breakln)

    var goback_button = document.createElement("input")
    goback_button.id = "goback_button";
    goback_button.type="button";
    goback_button.value = "Go Back";
    document.body.appendChild(goback_button);

    document.getElementById('goback_button').addEventListener("click", function(){sendDecision(false);});
}

function renderWaiting()
{
    document.body.innerHTML=""

    var h1 = document.createElement("h1");
    h1.textContent="Emeralds";
    document.body.appendChild(h1);

    var waitingP = document.createElement("p")
    waitingP.id = "waitingParagraph";
    waitingP.textContent="Relax and look at the screen :)";
    document.body.appendChild(waitingP);
}

function renderPressToContinute()
{
    document.body.innerHTML=""

    var h1 = document.createElement("h1");
    h1.textContent="Emeralds";
    document.body.appendChild(h1);

    var breakln = document.createElement("br")
    document.body.appendChild(breakln)

    var continue_button = document.createElement("input")
    continue_button.id = "continue_button";
    continue_button.type="button";
    continue_button.value = "Press if everyone is ready";
    document.body.appendChild(continue_button);

    document.getElementById("continue_button").addEventListener("click", function(){socket.send("continue"); renderWaiting();});
}