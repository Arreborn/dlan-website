/* some functions to manage the neat index page */

var targetDate = new Date("2023-05-12T21:00:00+02:00");
var currentTime = new Date().getTime();
var timeRemaining = targetDate.getTime() - currentTime;

function updateElementsText(text) {
    document.getElementById("current").innerHTML = text;
    document.getElementById("timer").innerHTML = text;
}

function getCurrentEventText(date) {
    if (date >= new Date("2023-05-12T21:00:00+02:00") && date < new Date("2023-05-12T23:00:00+02:00")) {
        return "Nästa turnering: Teamfight Tactics (23:00)";
    } else if (date >= new Date("2023-05-12T23:00:00+02:00") && date < new Date("2023-05-13T02:00:00+02:00")) {
        return "Pågående turnering: Teamfight Tactics";
    } else if (date >= new Date("2023-05-13T02:00:00+02:00") && date < new Date("2023-05-13T10:00:00+02:00")) {
        return "Nästa turnering: Schack (10:00)";
    } else if (date >= new Date("2023-05-13T10:00:00+02:00") && date < new Date("2023-05-13T13:00:00+02:00")) {
        return "Pågående turnering: Schack";
    } else if (date >= new Date("2023-05-13T13:00:00+02:00") && date < new Date("2023-05-13T14:00:00+02:00")) {
        return "Nästa turnering: League of Legends (14:00)";
    } else if (date >= new Date("2023-05-13T14:00:00+02:00") && date < new Date("2023-05-13T20:00:00+02:00")) {
        return "Pågående turnering: League of Legends";
    } else if (date >= new Date("2023-05-13T20:00:00+02:00") && date < new Date("2023-05-13T22:00:00+02:00")) {
        return "Pågående turnering: Super Smash Bros.";
    } else if (date >= new Date("2023-05-13T22:00:00+02:00") && date < new Date("2023-05-14T05:00:00+02:00")) {
        return "Pågående turnering: CS:GO";
    } else if (date >= new Date("2023-05-14T05:00:00+02:00") && date < new Date("2023-05-14T10:00:00+02:00")) {
        return "Alla turneringar för D-LAN 2023 är slut!";
    } else if (date >= new Date("2023-05-14T10:00:00+02:00")) {
        return "D-LAN 2023 har officiellt stängt. Tack för i år!";
    } else {
        return null;
    }
}

var timer = setInterval(function() {
    currentTime = new Date().getTime();
    timeRemaining = targetDate.getTime() - currentTime;

    var eventText = getCurrentEventText(currentTime);
    if (eventText) {
        updateElementsText(eventText);
        clearInterval(timer);
    } else {
        var seconds = Math.floor((timeRemaining / 1000) % 60);
        var minutes = Math.floor((timeRemaining / 1000 / 60) % 60);
        var hours = Math.floor((timeRemaining / (1000 * 60 * 60)) % 24);
        var days = Math.floor((timeRemaining / (1000 * 60 * 60 * 24)));

        seconds = seconds.toString().padStart(2, "0");
        minutes = minutes.toString().padStart(2, "0");
        hours = hours.toString().padStart(2, "0");

        document.getElementById("timer").innerHTML = "Tid kvar tills D-LAN: " + days + " dagar, " + hours + ":" + minutes + ":" + seconds + "!";
        timeRemaining -= 1000;
        if (timeRemaining < 0) {
            currentTime = new Date().getTime();
            eventText = getCurrentEventText(currentTime);
            if (eventText) {
                updateElementsText(eventText);
            } else {
                document.getElementById("timer").innerHTML = "D-LAN pågår just precis nu!";
            }
            clearInterval(timer);
        }
    }
}, 1000);


// hides intro on subsequent visits
// seems like it's broken :(
window.addEventListener("load", function () {
    var isFirstVisit = sessionStorage.getItem("isFirstVisit");
    console.log(isFirstVisit)
    if (!isFirstVisit) {
    sessionStorage.setItem("isFirstVisit", true);
    } else {
    document.getElementById("banner").classList.remove("show");
    }
    window.removeEventListener("load", arguments.callee);
});


