
header = `
    <div id="header-main">

        <div id="header-profile-picture">
            <img src="/static/images/profile-cat.jpg" alt="Profile Picture" />
        </div>

        <div id="header-title">
            <p>
                El Tamale Más Picante
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
            </ul>

        </nav>


    </div>
`

document.querySelector(".header").innerHTML = header;

var header_ul = document.getElementById("header-ul");
var menu_icon = document.querySelector(".menu-icon");


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
