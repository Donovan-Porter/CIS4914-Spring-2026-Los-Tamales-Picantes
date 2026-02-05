let gameId = null;
let matchCount = 0;
let clickedCards = [];
let waiting = false;
let boardSize = 4;

const boardDiv = document.getElementById("board");
const matchDiv = document.getElementById("match-count");
const statusDiv = document.getElementById("status");

// set up board after it fully loads
document.addEventListener("DOMContentLoaded", async () => {
    // set up a new game with size 4
    const res = await fetch("/matching", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ size: boardSize })
    });
    const data = await res.json();

    // save game ID
    gameId = data.game_id;

    // create col grid
    boardDiv.style.gridTemplateColumns = `repeat(${data.state.size}, 60px)`;

    // draw the cards on the board
    loadBoard(data.state);
});

function loadBoard(state) {
    // start fresh
    boardDiv.innerHTML = "";

    // loop through the entire board
    for (let eachRow = 0; eachRow < state.size; eachRow++) 
    {
        for (let eachCol = 0; eachCol < state.size; eachCol++) 
        {
            // create a clickable card
            const cardDiv = document.createElement("div");
            cardDiv.classList.add("card");

            // store the position
            cardDiv.dataset.row = eachRow;
            cardDiv.dataset.col = eachCol;

            // set card value
            cardDiv.innerText = state.board[eachRow][eachCol];

            // Check if there is a matched array
            if (state.matched) 
            {
                // make sure the row exists
                if (state.matched[eachRow]) 
                {
                    // is this card matched??
                    if (state.matched[eachRow][eachCol] === true) 
                    {
                        // change the match look
                        cardDiv.classList.add("matched");
                    }
                }
            }

            // add the click handle
            cardDiv.addEventListener("click", () => clickedCard(eachRow, eachCol, cardDiv));
            
            // add the card to the board
            boardDiv.appendChild(cardDiv);
        }
    }
}

// handle when the card is clicked
async function clickedCard(incomingRow, incomingCol, cardDiv) 
{
    // we are waiting
    // clicked the matched cards
    // clicking the same card
    if (waiting || 
        cardDiv.classList.contains("matched") || 
        clickedCards.includes(cardDiv)) 
    {
        return;
    }


    // show what cards are clicked visually
    clickedCards.push(cardDiv);
    cardDiv.classList.add("pending-match");


    // send the card to the backend
    const res = await fetch(`/matching/${gameId}/click`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row: incomingRow, col: incomingCol })
    });
    const result = await res.json();

    // the first card that is clicked returns none
    if (result.result === null ||
        clickedCards.length == 1) 
    {
        return;
    }

    // we are on to the second click now
    // locks the board while we are checking
    waiting = true;

    // we have a match
    if (result.result === "match") 
    {
        // increase the match count
        matchCount++;
        matchDiv.innerText = `Matches: ${matchCount}`;
        statusDiv.innerText = "MATCH";


        // change the cards to be matched colors
        clickedCards.forEach(c => {
            c.classList.remove("pending-match")
            c.classList.add("matched")}
        );
    } 

    // no match
    else 
    {
        statusDiv.innerText = "Not a match";

        // clear the pending visuals on the card
        clickedCards.forEach(c => c.classList.remove("pending-match"));
    }


    // clear the cards we are comparing
    clickedCards = [];

    // unlock the board
    waiting = false;

    // check if finished
    if (result.state.finished) 
    {
        statusDiv.innerText = "Game Done";
    }
}
