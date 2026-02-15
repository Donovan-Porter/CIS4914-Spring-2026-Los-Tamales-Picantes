var count = 3;
var interval = setInterval(function() {

    fetch('/toggleTimer', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.status);
        if (data.status === true)
        {
            document.getElementById('timer_title').textContent = "Time: ";
            document.getElementById('count').innerHTML = count;
            count--;
            if (count === -1)
            {
                clearInterval(interval);
                document.getElementById('count').innerHTML = 'Out of time!';
                document.querySelector("form").submit();
            }
        }
        else
        {
            clearInterval(interval);
            document.getElementById('count').innerHTML = "";
            document.getElementById('timer_title').textContent = "";
        }
    })
    .catch(error => {
        console.log('Error', error)
    });

}, 1000);
