// 1. Capturar elementos del DOM
const formulario = document.getElementById('formularioPedido');// Captura el formulario
const listaPedidos = document.getElementById('listaPedidos');// Captura el contenedor donde se mostrarán los pedidos
const contadorElemento = document.getElementById('contadorPedidos');// Captura el elemento donde se mostrará el contador de pedidos
let total = 0;

// 2. Escuchar el evento submit
formulario.addEventListener('submit', function(e) {
    e.preventDefault(); // Impide que la página se recargue

    // Obtener valores de los inputs
    const nombre = document.getElementById('nombreCliente').value;// Captura el valor del nombre del cliente
    const pez = document.getElementById('especiePez').value;// Captura el valor de la especie del pez
    const cantidad = document.getElementById('cantidad').value;// Captura el valor de la cantidad

    // Validación básica
    if (nombre === "" || pez === "" || cantidad === "") {
        alert("Por favor, completa todos los campos");
        return;
    }// Validación de cantidad

    // 3. Crear tarjeta (card) dinámicamente
    const divCol = document.createElement('div');// Crear un div para la columna
    divCol.className = "col-md-4";// Asignar clase de columna de Bootstrap
    divCol.innerHTML = `
        <div class="card h-100 border-0 shadow">
            <div class="card-body">
                <h5 class="card-title text-dark">${pez}</h5>
                <p class="card-text text-muted">Cliente: ${nombre}<br>Cantidad: ${cantidad}</p> <!-- Comentario: Mostrar información del pedido -->
                <button class="btn btn-danger btn-sm">Eliminar Pedido</button>      <!-- Botón para eliminar el pedido -->  
            </div>
        </div>  <!-- Comentario: Se crea una tarjeta con la información del pedido y un botón para eliminarlo -->
    `;

    // 4. Funcionalidad de eliminar
    divCol.querySelector('button').addEventListener('click', function() { // Escuchar el evento click del botón eliminar
        divCol.remove(); // Eliminar la tarjeta del DOM
        total--;
        contadorElemento.innerText = total;
    });// Escuchar el evento click del botón eliminar y actualizar el contador

    // 5. Insertar en el contenedor y actualizar contador
    listaPedidos.appendChild(divCol);// Agregar la tarjeta al contenedor de pedidos
    total++;
    contadorElemento.innerText = total;// Actualizar el contador de pedidos

    // Limpiar formulario
    formulario.reset();// Limpiar los campos del formulario después de enviar
});// Escuchar el evento submit del formulario y manejar la creación de pedidos