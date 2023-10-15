var isDragging = false;
var offset = { x: 0, y: 0 };
var windowElement = document.getElementById("myWindow");
var taskbarElement = document.querySelector(".taskbar");

function dragStart(event) {
  isDragging = true;
  offset.x = event.clientX - windowElement.offsetLeft;
  offset.y = event.clientY - windowElement.offsetTop;
}

function dragEnd(event) {
  isDragging = false;
}

function drag(event) {
  if (isDragging) {
    windowElement.style.left = (event.clientX - offset.x) + "px";
    windowElement.style.top = (event.clientY - offset.y) + "px";
  }
}

function closeWindow() {
  windowElement.style.display = "none";
}

function minimizeWindow() {
  windowElement.style.display = "none";
  var taskbarButton = document.createElement("button");
  taskbarButton.className = "taskbar-btn";
  taskbarButton.textContent = "Mi ventana";
  taskbarButton.onclick = function() {
    windowElement.style.display = "block";
    taskbarButton.remove();
  };
  taskbarElement.appendChild(taskbarButton);
}

function showInput() {
  var inputContainer = document.createElement("div");
  inputContainer.className = "input-container";
  var inputElement = document.createElement("input");
  inputElement.type = "text";
  inputElement.placeholder = "Nombre de la carpeta";
  var buttonElement = document.createElement("button");
  buttonElement.textContent = "Crear";
  buttonElement.onclick = function() {
    createFolder(inputElement.value);
    inputContainer.remove();
  };
  inputContainer.appendChild(inputElement);
  inputContainer.appendChild(buttonElement);

  windowElement.appendChild(inputContainer);
}



function createWindow() {
  // crea un nuevo elemento div para la ventana
  var newWindow = document.createElement("div");
  newWindow.classList.add("window");
  
  // establece un ID único para la ventana
  var windowId = "window-" + new Date().getTime();
  newWindow.setAttribute("id", windowId);
  
  // crea el contenido de la ventana
  var windowContent = `
    <div class="title-bar" onmousedown="dragStart(event)">
      <span class="title">Nueva ventana</span>
      <span class="minimize-btn" onclick="minimizeWindow()">-</span>
      <span class="close-btn" onclick="closeWindow()">X</span>
    </div>
    <div class="toolbar">
      <span class="new-folder-btn" onclick="showInput()">Nueva carpeta</span>
    </div>
    <div class="content">
      <div class="folder">
        <div class="folder-icon"></div>
        <div class="folder-label">Carpeta 1</div>
      </div>
      <div class="folder">
        <div class="folder-icon"></div>
        <div class="folder-label">Carpeta 2</div>
      </div>

      <div class="file">
        <div class="file-icon"></div>
        <div class="file-label">archivo.txt</div>
        <div class="file-size">Tamaño: 2.5 MB</div>
        <div class="file-modified-time">Modificado: 2023-06-28</div>
        <div class="file-access-time">Accedido: 2023-06-28</div>
        <div class="file-path">Ruta: /home/user/archivo.txt</div>
      </div>
    </div>
  `;
  
  // establece el contenido de la ventana
  newWindow.innerHTML = windowContent;
  
  // agrega la ventana al documento
  document.body.appendChild(newWindow);
}





window.addEventListener("mousemove", drag);
window.addEventListener("mouseup", dragEnd);