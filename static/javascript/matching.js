let gameId = null;
let matchCount = 0;
let clickedCards = [];
let waiting = false;

const boardDiv = document.getElementById("board");
const matchDiv = document.getElementById("match-count");
const statusDiv = document.getElementById("status");


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

    // work
    const working_chap = all_chap_num[spanish_select.value];

    let fill_in_chap = document.getElementById("chp_num");
    // clear the dropdown
    fill_in_chap.innerHTML = "";

    // add each chapter option
    for (const num of working_chap)
    {
        // create an option
        const option = document.createElement("option");
        option.value = num;
        option.innerText = `Chapter ${num}`;
        // add it on the html side
        fill_in_chap.appendChild(option);
    }
}


// change the course selection 
const vocab_select = document.getElementById("vocab_select");
vocab_select.addEventListener("change", update_course_options);
function update_course_options()
{
    const course_options = {
        Vocabulary: [
            {value: "spn1130", text: "Spainsh 1130"},
            {value: "spn1131", text: "Spainsh 1131"},
            {value: "spn2200", text: "Spainsh 2200"},
            {value: "spn2201", text: "Spainsh 2201"}],
        Grammar: [
            {value: "spn1130", text: "Spainsh 1130"}]};

    // work
    const working_list = course_options[vocab_select.value];

    const spn_options = document.getElementById("spn_lvl");
    // clear the dropdown
    spn_options.innerHTML = "";

    // add each course option
    for (const course of working_list)
    {
        // create an option
        const option = document.createElement("option");
        option.value = course.value;
        option.innerText = course.text;
        // add it on the html side
        spn_options.appendChild(option);
    }

    // then update the chapter numbers too
    update_chap_numbers();
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
            file_type: document.getElementById("vocab_select").value})
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
    }
}

