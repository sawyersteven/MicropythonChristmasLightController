let $currentPlayingDisplay = null;
let $seqSelect = null;
let $speedSelect = null;
let $progBar = null;
let $btnSetSeq = null;
let $footer = null;
let $btnSetDefault = null;

let SequenceList = null;

const Speed = {
    500: 'Fast',
    1000: 'Normal',
    2000: 'Slow'
};

window.addEventListener('load', (event) => {
    $currentPlayingDisplay = document.getElementById('currentPlaying');
    $progBar = document.getElementById('refreshTimerBar');
    $seqSelect = document.getElementById('seqSelect');
    $speedSelect = document.getElementById('speedSelect');
    $btnSetSeq = document.getElementById('btnSetSeq');
    $footer = document.getElementsByTagName("footer")[0];
    $btnSetDefault = document.getElementById("btnSetDefault");

    SequenceList = JSON.parse(document.getElementById("sequencelist").textContent);

    SequenceList.forEach((e, i) => {
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = e;
        $seqSelect.appendChild(opt);
    });
    getStatus();
});

let progbarValue = 0;
async function startNewRefreshTimer() {
    await new Promise(r => setTimeout(r, 500));
    progbarValue = 0;
    $progBar.value = progbarValue;
    let progBarInterval = setInterval(() => {
        progbarValue += 5;
        $progBar.value = progbarValue;
        if (progbarValue >= 100) {
            getStatus();
            clearInterval(progBarInterval);
        }
    }, 100);
}

function getStatus() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/status');
    xhr.send();
    xhr.ontimeout = () => {
        $currentPlayingDisplay.value = 'Lost connection...';
        startNewRefreshTimer();
    };
    xhr.onerror = () => {
        $currentPlayingDisplay.value = 'Lost connection...';
        startNewRefreshTimer();
    };
    xhr.onload = () => {
        handleStatusJson(xhr.responseText);
    }
}

function setSeq() {
    $btnSetSeq.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/setsequence');
    xhr.setRequestHeader('Content-Type', 'application/json');
    let payload = JSON.stringify({ 'newSequenceID': parseInt($seqSelect.value), 'newSpeed': $speedSelect.value });
    xhr.send(payload);
    xhr.ontimeout = () => {
        $currentPlayingDisplay.value = 'Lost connection to controller...';
        $btnSetSeq.disabled = false;
    };
    xhr.onerror = (e) => {
        $currentPlayingDisplay.value = e.message;
        $btnSetSeq.disabled = false;
    };
    xhr.onload = () => {
        handleStatusJson(xhr.responseText);
    }
}

function setDefault() {
    $btnSetDefault.disabled = true;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/setdefault');
    xhr.setRequestHeader('Content-Type', 'application/json');
    let payload = JSON.stringify({ 'sequenceID': parseInt($seqSelect.value), 'speed': $speedSelect.value });
    xhr.send(payload);
    xhr.ontimeout = () => {
        $footer.textContent = "Request timed out...";
        $btnSetDefault.disabled = false;
    };
    xhr.onerror = (e) => {
        $footer.textContent = e.message;
        $btnSetDefault.disabled = false;
    };
    xhr.onload = () => {
        try {
            let jsonResponse = JSON.parse(xhr.responseText);
            $footer.textContent = "Default sequence set to " + SequenceList[jsonResponse['newDefaultSeq']] + " " + Speed[jsonResponse['newDefaultSpeed']];
        } catch (err) {
            $footer.textContent = err;
        } finally {
            $btnSetDefault.disabled = false;
        }
    }
}
function handleStatusJson(plaintext) {
    try {
        let jsonResponse = JSON.parse(plaintext);
        $currentPlayingDisplay.value = SequenceList[jsonResponse['nowPlayingID']] + " | " + Speed[jsonResponse['speed']];
        $footer.textContent = "";
    } catch (err) {
        $footer.textContent = err;
    } finally {
        $btnSetSeq.disabled = false;
        startNewRefreshTimer()
    }
}