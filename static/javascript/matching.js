let gameId = null;
let matchCount = 0;
let clickedCards = [];
let waiting = false;

const boardDiv = document.getElementById("board");
const matchDiv = document.getElementById("match-count");
const statusDiv = document.getElementById("status");
const homeDiv = document.getElementById('return-button');

// const difficultyButtons = document.querySelectorAll(".difficulty-button");
// // set the input board size based on diffculty
// difficultyButtons.forEach(button => {
//     button.addEventListener("click", () => {
//         let board_size;
//         if (button.innerText === "TEST")
//         { 
//             board_size = 2;
//         }        
//         if (button.innerText === "Easy")
//         { 
//             board_size = 4;
//         }
//         else if (button.innerText === "Medium") 
//         { 
//             board_size = 6;
//         }

//         else if (button.innerText === "Hard")
//         { 
//             board_size = 8;
//         }

//         // setupBoard(board_size);
//     });
// });


// redirect to home page
document.getElementById('home-button').onclick = function() { window.location.href = '/'; };


// change the chapter selection 
const spanish_select = document.getElementById("spn_lvl");
spanish_select.addEventListener("change", update_chap_numbers);
function update_chap_numbers()
{
    const all_chap_num = {
        spn1130: [1, 2, 3, 4, 5, 6],
        spn1131: [7, 8, 9, 10, 11, 12],
        spn2200: [13, 14, 15, 16, 17, 18],
        spn2201: [19, 20, 21, 22, 23, 24]};

    const fill_in_chap = document.getElementById("chp_num");

    // work
    const working_chap = all_chap_num[spanish_select.value];

    // clear the dropdown
    fill_in_chap.innerHTML = "";

    // add each chapter option
    for (num of working_chap)
    {
        // create an option
        option = document.createElement("option");
        option.value = num;
        option.innerText = `Chapter ${num}`;
        // add it on the html side
        fill_in_chap.appendChild(option);
    }
}


function get_board_size()
{
    const level = document.getElementById("spn_lvl").value;

    switch (level)
    {
        case "spn1130":
            return 4;
        case "spn1131":
            return 6;
        case "spn2200":
            return 8;
        case "spn2201":
            return 8;
        default:
            return 4;
    }
}

// send the file parts to the game
document.getElementById('load-file').onclick = parse_the_file_info_and_setup;
async function parse_the_file_info_and_setup()
{
    // reset everything on a new load
    matchCount = 0;
    clickedCards = [];
    waiting = false;
    matchDiv.innerText = `Matches: ${matchCount}`;
    homeDiv.style.display = "none";
    statusDiv.innerText = "";

    // send the info to set up a new game
    const board_size = get_board_size();

    const res = await fetch("/matching", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            size: board_size , 
            spanish_level: document.getElementById("spn_lvl").value,
            chapter_number: document.getElementById("chp_num").value,
            is_vocab: document.getElementById("vocab_select").value})
    });
    const data = await res.json();

    // save game ID
    gameId = data.game_id;

    // create col grid
    boardDiv.style.gridTemplateColumns = `repeat(${data.state.size}, 60px)`;

    // draw the cards on the board
    loadBoard(data.state);
}


function loadBoard(state) 
{
    // remove the old board
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
        clickedCards.forEach(card => {
            card.classList.remove("pending-match")
            card.classList.add("matched")}
        );
    } 

    // no match
    else 
    {
        statusDiv.innerText = "Not a match";

        // clear the pending visuals on the card
        clickedCards.forEach(card => card.classList.remove("pending-match"));
    }


    // clear the cards we are comparing
    clickedCards = [];

    // unlock the board
    waiting = false;

    // check if finished
    if (result.state.finished) 
    {
        // display that it is done
        statusDiv.innerText = "Game Done";

        // show the home button
        homeDiv.style.display = 'block';
    }
}

