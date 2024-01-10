// graphCanvas.js

// various parameters, can be tweaked
var canvasWidth = 800;
var canvasHeight = 600;

var graphMinX = 100;
var graphMaxX = 800;
var lowestX = graphMinX; // the furthest left point aligns with the left edge of the graph
var highestX = graphMaxX-50; // the furthest right point does not align, for mouseover reasons
var graphMinY = 50;
var graphMaxY = 550;
var lowestY = graphMinY;// + 25; 
var highestY = graphMaxY;// - 25;

// list all notes from A1 to G#8
var notes = [];
var noteValues = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F",
                  "F#", "G", "G#"];

var lowestPitch = -1;
var highestPitch = -1;
var maxTime = -1;

// colors is a dict mapping note names to colors
var colors = {};
colors["A"] = "#FF0000";
colors["A#"] = "#FF8000";
colors["B"] = "#FFFF00";
colors["C"] = "#80FF00";
colors["C#"] = "#00FF00";
colors["D"] = "#00FF80";
colors["D#"] = "#00FFFF";
colors["E"] = "#0080FF";
colors["F"] = "#0000FF";
colors["F#"] = "#8000FF";
colors["G"] = "#FF00FF";
colors["G#"] = "#FF0080";

for (var i = 1; i <= 8; i++) {
    for (var j = 0; j < noteValues.length; j++) {
        notes.push(noteValues[j] + i);
    }
}

function pitchToValue(pitch) { // maps pitch to a given value
    // 440 = A4 maps to 0. B4 maps to 1, G#3 maps to -1, A5 maps to 12, etc.
    return Math.log2(pitch / 440) * 12;
}

function valueToPitch(value) { // maps a given value to a pitch
    return Math.pow(2, value / 12) * 440;
}

function pitchToNote(pitch) {
    var value = pitchToValue(pitch);
    var note = notes[Math.round(value) + 36];
    return note;
}

function timeToX(time, maxTime) { // returns the x position of a given time
    var actualX = time / maxTime;
    var x = lowestX + (highestX - lowestX) * actualX;
    return x;
}

function pitchToY(pitch, lower, upper) { // returns the y position of a given pitch
    var value = pitchToValue(pitch);
    var actualY = (value - lower) / (upper - lower);
    var y = highestY - (highestY - lowestY) * actualY;
    return y;
}

function YToPitch(y, lower, upper) { // returns the pitch of a given y position
    var YRatio = (highestY - y) / (highestY - lowestY);
    var YValue = YRatio * (upper - lower) + lower;
    console.log(YValue);
    var pitch = valueToPitch(YValue);
    return pitch;
}

function generateCanvas(ctx, pitches) {
    // draw the points
    var timeArray = [];
    var pitchArray = [];
    for (var i = 0; i < pitches.length; i++) {
        timeArray.push(pitches[i][0]);
        pitchArray.push(pitches[i][1]);
    }

    // draw axes in blue
    ctx.lineWidth = 6;
    ctx.fillStyle = "#0000FF";
    ctx.beginPath();
    ctx.moveTo(graphMinX, graphMinY);
    ctx.lineTo(graphMinX, graphMaxY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(graphMinX, graphMaxY);
    ctx.lineTo(graphMaxX, graphMaxY);
    ctx.stroke();

    // label axes
    ctx.textAlign = "center";
    ctx.font = "20px Arial";
    ctx.fillText("Time (seconds)", (graphMinX + graphMaxX) / 2, graphMaxY + 25);

    // draw points in black, as well as bottom left corner
    ctx.fillStyle = "#000000";
    ctx.arc(graphMinX, graphMaxY, 3, 0, 2 * Math.PI);
    ctx.fill();
    maxTime = Math.max(...timeArray);
    
    lowestPitch = pitchToValue(Math.min(...pitchArray));
    highestPitch = pitchToValue(Math.max(...pitchArray));
    
    var lowestNote = Math.floor(lowestPitch-0.5)+0.5;
    var highestNote = Math.floor(highestPitch-0.5)+1.5;
    
    // colored rects and gray divider lines
    for (var i = lowestNote+1; i <= highestNote; i += 1) {
        ctx.lineWidth = 2;
        var y = pitchToY(Math.pow(2, i/12) * 440, lowestPitch, highestPitch);
        var y_old = pitchToY(Math.pow(2, (i-1)/12) * 440, lowestPitch, highestPitch);
        // create rectangle from y_old to y
        var pitch = pitchToNote(Math.pow(2, (i-0.5)/12) * 440);
        ctx.fillStyle = colors[pitch.substring(0, pitch.length-1)];
        ctx.beginPath();
        // log y, y_old
        console.log(y, y_old);
        if (y > graphMinY) {
            ctx.fillRect(graphMinX, Math.min(y_old, graphMaxY), graphMaxX-graphMinX, y - Math.min(y_old, graphMaxY));
            ctx.fillStyle = "#AAAAAA";
            ctx.beginPath();
            ctx.moveTo(graphMinX, y);
            ctx.lineTo(graphMinX + graphMaxX, y);
            ctx.stroke();
        } else {
            ctx.fillRect(graphMinX, Math.min(y_old, graphMaxY), graphMaxX-graphMinX, graphMinY - Math.min(y_old, graphMaxY));
        }
       
    }

    ctx.font = "12px Arial";
    ctx.fillStyle = "#000000";
    for (var i = 0; i < pitches.length; i++) {
        var actualX = timeArray[i];
        actualX = actualX / maxTime;
        var x = lowestX + (highestX - lowestX) * actualX;
        // scale pitchesX, pitchesY into a [0, 1] range
        //var actualY = pitchToValue(pitchArray[i]);
        //actualY = (actualY - lowestPitch) / (highestPitch - lowestPitch);
        // var y = highestY - (highestY - lowestY) * actualY;
        var y = pitchToY(pitchArray[i], lowestPitch, highestPitch);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
        ctx.fillText(pitchToNote(pitchArray[i]), x, y - 10);
    }

}

function handleMouseMove(event) {
    if (Math.min(lowestPitch, highestPitch, maxTime) == -1) {
        return;
    }
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    const coordinatesElement = document.getElementById("coordinates");
    var time = (mouseX - graphMinX) / (graphMaxX - graphMinX) * maxTime;
    var pitch = YToPitch(mouseY, lowestPitch, highestPitch);
    // round to 2 decimal places
    time = Math.round(time * 100) / 100;
    pitch = Math.round(pitch * 100) / 100;
    coordinatesElement.textContent = "Time: " + time + ", Pitch: " + pitch;
}