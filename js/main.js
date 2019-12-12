function listarPiadas() {
    document.getElementById('lista').innerHTML = '';
    fetch("http://localhost:5000/piadasnerd")
      .then(response => response.json())
      .then(json => {
        console.log(json)
        json.piadas.forEach(
          piada => {
            console.log(piada)
  
            var ul = document.getElementById("lista");
            var li = document.createElement('li');
            var span = document.createElement('span');
            span.classList.add('mdl-list__item-primary-content')
            var i = document.createElement('i');
            i.classList.add('material-icons')
            i.classList.add('mdl-list__item-avatar')
            i.textContent = 'insert_emoticon'
  
            let pergunta = document.createElement('span')
            pergunta.textContent = piada.pergunta
            let resposta = document.createElement('span')
            resposta.classList.add('mdl-list__item-text-body')
            resposta.textContent = piada.resposta
  
  
            span.appendChild(i)
            span.appendChild(pergunta)
            span.appendChild(resposta)
  
            li.classList.add("mdl-list__item");
            li.classList.add("mdl-list__item--three-line");
            li.appendChild(span);
            ul.appendChild(li);
          }
        )
      })
      .catch(erro => console.log(erro));
  }
  
  function save() {
  
    var data = {};
    data.id = document.getElementById('id').value;
    data.pergunta = document.getElementById('pergunta').value;
    data.resposta = document.getElementById('resposta').value;
  
    var url = `http://localhost:5000/piadasnerd/${data.id}`;
  
    console.log(`url: ${url}`)
  
    var json = JSON.stringify(data);
    var request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    request.onload = function () {
      var users = JSON.parse(request.responseText);
      if (request.readyState == 4 && request.status == "201") {
        console.table(users);
      } else {
        console.error(users);
      }
    }
    request.send(json);
  }