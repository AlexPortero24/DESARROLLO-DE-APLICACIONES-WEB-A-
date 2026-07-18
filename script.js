// ==========================================================
// SEMANA 7 - DATOS Y RENDERIZADO DE PRODUCTOS
// ==========================================================

// 1. DATOS DE PRODUCTOS (Arreglo de objetos)
const productosCatalogo = [
    {
        id: 1,
        nombre: 'Peces y Plantas',
        icono: 'bi-water',
        items: [
            'Peces exóticos de agua dulce (Betas, Guppys, Goldfish y Ángeles).',
            'Sustratos nutritivos y plantas naturales para acuarios plantados.'
        ]
    },
    {
        id: 2,
        nombre: 'Equipamiento e Iluminación',
        icono: 'bi-gear-fill',
        items: [
            'Peceras de vidrio de alta resistencia y acuarios a la medida.',
            'Sistemas de filtración avanzados (cascada, internos y canister).',
            'Bombas de oxígeno, aireadores y motores de flujo.',
            'Sistemas de iluminación LED de bajo consumo energético.'
        ]
    },
    {
        id: 3,
        nombre: 'Nutrición y Asesoría',
        icono: 'bi-heart-pulse-fill',
        items: [
            'Alimentos premium en hojuelas, pellets y suplementos.',
            'Accesorios ecológicos y troncos naturales.',
            'Asesoría personalizada en el ciclado del agua y control de parámetros.'
        ]
    }
];

// 2. FUNCIÓN PARA RENDERIZAR PRODUCTOS
function renderizarProductos() {
    const contenedor = document.getElementById('contenedor-productos');
    
    // Limpiar el contenedor
    contenedor.innerHTML = '';
    
    // Recorrer el arreglo de productos y crear tarjetas
    productosCatalogo.forEach(producto => {
        const col = document.createElement('div');
        col.className = 'col';
        col.innerHTML = `
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body p-4">
                    <div class="mb-3 text-info fs-1">
                        <i class="bi ${producto.icono}"></i>
                    </div>
                    <h4 class="card-title fw-bold text-dark mb-3">${producto.nombre}</h4>
                    <ul class="card-text text-secondary small ps-3">
                        ${producto.items.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
        contenedor.appendChild(col);
    });
}

// ==========================================================
// SEMANA 6 - VALIDACIONES Y GESTIÓN DE PEDIDOS 
// ==========================================================
// 1. Capturar elementos del DOM
const formulario = document.getElementById('formularioPedido');// Captura el formulario
const listaPedidos = document.getElementById('listaPedidos');// Captura el contenedor donde se mostrarán los pedidos
const contadorElemento = document.getElementById('contadorPedidos');// Captura el elemento donde se mostrará el contador de pedidos
let total = 0;

// 1.1 Validaciones dinámicas en tiempo real semana 6
document.getElementById('nombreCliente').addEventListener('input', function() {
    if (this.value.trim().length >= 3) {
        this.classList.remove('is-invalid'); // Quita el rojo si ya está correcto
    }
});
// Validación para la especie del pez
document.getElementById('especiePez').addEventListener('input', function() {
    if (this.value.trim().length > 0) {
        this.classList.remove('is-invalid');
    }
});

// Validación para la cantidad
document.getElementById('cantidad').addEventListener('input', function() {
    if (this.value > 0) {
        this.classList.remove('is-invalid');
    }
}); // Fin de validaciones dinámicas semana 6

// SEMANA 6 - VALIDACIONES DE AVISO INMEDIATO (Si escribe algo mal)
// ==========================================================
document.getElementById('nombreCliente').addEventListener('input', function() {
    if (this.value.trim().length > 0 && this.value.trim().length < 3) {
        this.classList.add('is-invalid'); // Pone rojo si empieza a escribir menos de 3
    }
});

document.getElementById('especiePez').addEventListener('input', function() {
    if (this.value.trim().length === 0) {
        this.classList.add('is-invalid'); // Pone rojo si borra todo
    }
});

document.getElementById('cantidad').addEventListener('input', function() {
    if (this.value !== "" && this.value <= 0) {
        this.classList.add('is-invalid'); // Pone rojo si escribe un número menor a 1
    }
});
// ==========================================================


// 2. Escuchar el evento submit
formulario.addEventListener('submit', function(e) {
    e.preventDefault(); // Impide que la página se recargue

    // Obtener valores de los inputs
    // 1. CAPTURAR LOS ELEMENTOS (sin el .value al final)
    const inputNombre = document.getElementById('nombreCliente');// Captura el input del nombre del cliente
    const inputPez = document.getElementById('especiePez'); // Captura el input de la especie del pez
    const inputCantidad = document.getElementById('cantidad'); // Captura el input de la cantidad de peces
     
// semana 6 inicio 
let esValido = true; // Variable de control
    // Validar nombre
    if (inputNombre.value.trim().length < 3) {
        inputNombre.classList.add('is-invalid');
        esValido = false;
    } else {
        inputNombre.classList.remove('is-invalid');
    }

    // Validar pez
    if (inputPez.value.trim() === "") {
        inputPez.classList.add('is-invalid');
        esValido = false;
    } else {
        inputPez.classList.remove('is-invalid');
    }

    // Validar cantidad
    if (inputCantidad.value <= 0 || inputCantidad.value === "") {
        inputCantidad.classList.add('is-invalid');
        esValido = false;
    } else {
        inputCantidad.classList.remove('is-invalid');
    }

    // Si algo falló, detenemos la ejecución aquí
    if (!esValido) return;
//semnana 6 fin


    // Validación básica
    if (inputNombre.value === "" || inputPez.value === "" || inputCantidad.value === "") {
        alert("Por favor, completa todos los campos");
        return;
    }// Validación de cantidad

    // 3. Crear tarjeta (card) dinámicamente
    const divCol = document.createElement('div');// Crear un div para la columna
    divCol.className = "col-md-4";// Asignar clase de columna de Bootstrap
    divCol.innerHTML = `
        <div class="card h-100 border-0 shadow">
            <div class="card-body">
                <h5 class="card-title text-dark">${inputPez.value}</h5>
                <p class="card-text text-muted">Cliente: ${inputNombre.value}<br>Cantidad: ${inputCantidad.value}</p> <!-- Comentario: Mostrar información del pedido -->
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

    // Limpiar formulario y quitar clases de validación
    formulario.reset();// Limpiar los campos del formulario
    document.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));// Quitar la clase de validación de todos los inputs
});// Escuchar el evento submit del formulario y manejar la creación de pedidos

// ==========================================================
// INICIALIZAR CONTENIDO AL CARGAR LA PÁGINA
// ==========================================================

document.addEventListener('DOMContentLoaded', function() {
    // Renderizar productos del catálogo
    renderizarProductos();
    
    console.log('✅ Productos renderizados dinámicamente desde JavaScript');
    console.log('📦 Total de productos:', productosCatalogo.length);
});
