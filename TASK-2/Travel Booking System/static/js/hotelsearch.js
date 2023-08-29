document.addEventListener("DOMContentLoaded", () => {
    flight_duration();
    filter_price();
    document.querySelector(".clr-filter-div button").addEventListener('click', reset_filter);

    initial_click();
    tab_change();
    flight_select();


});

function flight_duration() {
    document.querySelectorAll(".flight-stops .tooltiptext").forEach(element => {
        let time = element.dataset.value.split(":");
        element.innerText = time[0]+"h "+time[1]+"m";
    });
}

function flight_duration2() {
    document.querySelectorAll(".flight-stops2 .tooltiptext").forEach(element => {
        let time = element.dataset.value.split(":");
        element.innerText = time[0]+"h "+time[1]+"m";
    });
}


function filter(element=null) {
    filter_price();
}


function filter2(element=null) {
    filter_price2();
}

function filter_price() {
    let value = document.querySelector(".filter-price input[type=range]").value;
    document.querySelector(".filter-price .final-price-value").innerText = value;

    let div = document.querySelector("#flights_div");
    let hotels = div.querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < hotels.length; i++) {
        if (parseInt(hotels[i].querySelector(".flight-price span").innerText) > parseInt(value)) {
            hotels[i].classList.add('hide');
            hotels[i].classList.remove('show');
        } else {
            hotels[i].classList.add('show');
            hotels[i].classList.remove('hide');
        }
    }
}

function reset_filter() {
    let max = document.querySelector(".filter-price input[type=range]").getAttribute('max');
    document.querySelector(".filter-price input[type=range]").value = max;
    document.querySelector(".filter-price .final-price-value").innerText = max;

    let hotels = document.querySelector("#flights_div").querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < hotels.length; i++) {
        hotels[i].classList.add('show');
        hotels[i].classList.remove('hide');
    }
}


function filter_price2() {
    let value = document.querySelector(".filter-price2 input[type=range]").value;
    document.querySelector(".filter-price2 .final-price-value").innerText = value;

    let div = document.querySelector("#flights_div2");
    let flights = div.querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < flights.length; i++) {
        if (flights[i].querySelector(".flight-price span").innerText > parseInt(value)) {
            flights[i].classList.add('hide');
            flights[i].classList.remove('show');
        }
        else {
            flights[i].classList.add('show');
            flights[i].classList.remove('hide');
        }
    }
    
}

function reset_filter2() {
    let max = document.querySelector(".filter-price2 input[type=range]").getAttribute('max');
    document.querySelector(".filter-price2 input[type=range]").value = max;
    document.querySelector(".filter-price2 .final-price-value").innerText = max;

    let flights = document.querySelector("#flights_div2").querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < flights.length; i++) {
            flights[i].classList.add('show');
            flights[i].classList.remove('hide');
    }
}

function trip_type_flight(element) {
    if(element.dataset.trip_type === '1') {
        document.querySelector(".query-result-div-2").style.display = 'none';
        document.querySelector(".query-result-div").style.display = 'block';
    }
    else if(element.dataset.trip_type === '2') {
        document.querySelector(".query-result-div").style.display = 'none';
        document.querySelector(".query-result-div-2").style.display = 'block';
    }
}

function flight_select() {
    document.querySelectorAll(".flight1-radio").forEach(radio => {
        radio.addEventListener('click', e => {
            document.querySelectorAll('#flt1').forEach(flt1 => {
                flt1.value = e.target.value;
            });
            document.querySelector("#select-f1-plane").innerText = e.target.dataset.plane;
            document.querySelector("#select-f1-depart").innerText = e.target.dataset.depart;
            document.querySelector("#select-f1-arrive").innerText = e.target.dataset.arrive;
            document.querySelector("#select-f1-fare").innerText = e.target.dataset.fare;
            document.querySelector("#select-total-fare").innerText = parseInt(e.target.dataset.fare) + parseInt(document.querySelector("#select-f2-fare").innerText);
            document.querySelector("#select-total-fare-media").innerText = parseInt(e.target.dataset.fare) + parseInt(document.querySelector("#select-f2-fare").innerText);
        });
    });
    document.querySelectorAll(".flight2-radio").forEach(radio => {
        radio.addEventListener('click', e => {
            document.querySelectorAll('#flt2').forEach(flt2 => {
                flt2.value = e.target.value;
            })
            document.querySelector("#select-f2-plane").innerText = e.target.dataset.plane;
            document.querySelector("#select-f2-depart").innerText = e.target.dataset.depart;
            document.querySelector("#select-f2-arrive").innerText = e.target.dataset.arrive;
            document.querySelector("#select-f2-fare").innerText = e.target.dataset.fare;
            document.querySelector("#select-total-fare").innerText = parseInt(e.target.dataset.fare) + parseInt(document.querySelector("#select-f1-fare").innerText);
            document.querySelector("#select-total-fare-media").innerText = parseInt(e.target.dataset.fare) + parseInt(document.querySelector("#select-f1-fare").innerText);
        });
    });
}

function media_click(element) {
    if (window.matchMedia("(max-width: 376px)").matches) {
        if (document.querySelector('#trip-identifier').value === '1') {
            element.querySelector('.o-b').click();
        }
        else {
            element.querySelector('.r-b').click();
            element.parentElement.parentElement.querySelectorAll('.blue').forEach(flt => {
                flt.classList.remove('blue');
            });
            element.classList.add('blue');
        }
    }
    else {
        return;
    }
}

function initial_click() {
    if (window.matchMedia("(max-width: 376px)").matches) {
        if (document.querySelector('#trip-identifier').value === '2'){
            document.querySelector(".query-result-div .each-flight-div").classList.add('blue');
            document.querySelector(".query-result-div-2 .each-flight-div").classList.add('blue');
        }
    }
}

function show_filter() {
    if(Boolean(document.querySelector(".query-result-div-2"))) {
        let r1 = document.querySelector(".query-result-div");
        let r2 = document.querySelector(".query-result-div-2");
        if(r2.style.display === 'none') {
            r1.querySelector(".filter-div").style.display = 'block';
            r2.querySelector(".filter-div").style.display = 'none';
        }
        else {
            r2.querySelector(".filter-div").style.display = 'block';
            r1.querySelector(".filter-div").style.display = 'none';
        }
    }
    else {
        document.querySelector(".query-result-div .filter-div").style.display = 'block';
    }
}

function tab_change() {
    var tabs = $('.tabs');
    var selector = $('.tabs').find('a').length;
    //var selector = $(".tabs").find(".selector");
    var activeItem = tabs.find('.active-div');
    var activeWidth = activeItem.innerWidth();
    $(".selector").css({
    "left": activeItem.position.left + "px", 
    "width": activeWidth + "px"
    });

    $(".tabs").on("click","a",function(e){
    e.preventDefault();
    $('.tabs a').removeClass("active-div");
    $(this).addClass('active-div');
    var activeWidth = $(this).innerWidth();
    var itemPos = $(this).position();
    $(".selector").css({
        "left":itemPos.left + "px", 
        "width": activeWidth + "px"
    });
    setTimeout(() => {trip_type_flight(e.target);},400);
    });
}
