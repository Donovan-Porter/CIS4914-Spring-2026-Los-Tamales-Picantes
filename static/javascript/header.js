
header = `
    <div id="header-main">

        <div id="header-profile-picture">
            <img src="/static/images/profile-cat.jpg" alt="Profile Picture" />
        </div>

        <div id="header-title">
            <p>
                Hot Tamales Spanish
            </p>
        </div>

        <nav>

            <div id="menu-icon">
                <img src="/static/images/ellipsis-vertical.png" alt="Menu Options" />
            </div>

            <ul id="header-ul">
                <a href="/" title="Home">
                    Home
                </a>
                <a href="/chat" title="Chat">
                    Chat
                </a>
                <a href="/translate" title="Translate">
                    Translate

                <a href="/matching_page" title="Matching Game">
                    Matching Game
                </a>
            </ul>

        </nav>

    </div>

    <style>
        #header-main {
            background: #76BA9D;
            display: flex;
            align-items: stretch;
            justify-content: space-between;

            height: 10vh;
        }

        #header-title {
            font-family: 'Trebuchet', sans-serif;
            font-size: 40px;
            font-weight: bold;
            color: #04361D; 
            align-self: center;
            margin-right: 55vw;
            
        }
                
        #header-profile-picture
        {
            height: 10vh;
        }

        #header-profile-picture img
        {
            height: 10vh;
        }

        #header-title:hover
        {
            cursor: default;
        }

        #header-main nav
        {
            height: 10vh;
        }

        #header-main nav #menu-icon
        {
            height: 10vh;
            z-index: 80;
        }

        #header-main nav #menu-icon img
        {
            height: 10vh;
        }

        #header-main nav #menu-icon:hover
        {
            background-color: #30303058;
            cursor: pointer;
            color: #80a8d0;
        }

        #header-main nav #menu-icon:active
        {
            color: #80d0a8;
        }

        #header-main nav ul
        {
            font-size: 20px;

            background-color: #30305880;
            border-radius: 25px;
            border: 1px solid;

            list-style-type: none;
            margin: 0;
            padding: 0;

            display: flex;
            flex-direction: column;
            align-items: center;

            position: absolute;
            top: 10vh;
            right: 0;

            transform-origin: 50% 0%;
            transform: scaleY(0);

            z-index: 79;
            transition: 0.5s;
        }

        #header-main nav ul a
        {
            margin: 5px;
        }

    </style>
`

document.querySelector(".header").innerHTML = header;

var header_ul = document.getElementById("header-ul");
var menu_icon = document.querySelector("#menu-icon");


menu_icon.addEventListener("click", menuToggle);


function menuToggle()
{

    if (header_ul.style.transform == "scaleY(1)")
    {
        header_ul.style.transform = "scaleY(0)";
    }
    else
    {
        header_ul.style.transform = "scaleY(1)";
    }
}
