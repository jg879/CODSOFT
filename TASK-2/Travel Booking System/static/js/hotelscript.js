function showCitiesList(input) {
    let cityList = input.parentElement.querySelector(".places_box");
    cityList.style.display = 'block';
}

function hideCitiesList(input) {
    let cityList = input.parentElement.querySelector(".places_box");
    setTimeout(() => {
        cityList.style.display = 'none';
    }, 300);
}

function selectCity(option) {
    let input = option.parentElement.parentElement.querySelector('input[type=text]');
    input.value = option.dataset.value.toUpperCase();
    input.dataset.value = option.dataset.value;
    hideCitiesList(input);
}
