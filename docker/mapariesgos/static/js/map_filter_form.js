const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const form = document.querySelector('#map-filter-form');

function sendForm(event){
    event.preventDefault();
    const request = new Request(
        "{% url 'api:filtrar_incidentes' %}",{
            method: 'GET',
            headers: {'X-CSRFToken': csrfToken},
            mode: 'same-origin'
        }
    );
    fetch(request)
        .then((request => {
            if (request.ok){
                return request.json();
            }
            throw new Error('No recibi respuesta del servidor');
        })
        .then(function(data) {
            console.log(data);
            if (data.status === 'ok') {
                alert('Todo bien');
            } else{
                alert('Error');
            }
        }));
}
form.addEventListener('submit', sendForm);