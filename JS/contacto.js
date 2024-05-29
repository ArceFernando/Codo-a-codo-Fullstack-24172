let persona = document.querySelector("#Persona");
let personaCopia = persona.cloneNode(true);

let contenedor = document.querySelector("main");

persona.remove()

fetch("https://randomuser.me/api")
.then(response => response.json())
.then(data => {
   let nuevaPersona = personaCopia.cloneNode(true);

   nuevaPersona.querySelector("#Foto").src=data.results[0].picture.large;
   nuevaPersona.querySelector("#Foto").alt="Foto Club";
   nuevaPersona.querySelector("#Nombre").innerHTML = data.results[0].name.first+ " "+ data.results[0].name.last;
   
   contenedor.appendChild(nuevaPersona);
   
   console.log(data.results[0].name.first + " " + data.results[0].name.last);
});

let titulo =document.getElementById("Titulo");

titulo.innerHTML = "Este ha sido alterado por JS"

console.log(titulo);