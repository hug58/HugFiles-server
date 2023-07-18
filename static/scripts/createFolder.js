function selectFolder(folder){
    //TODO: get files from folder
}

function createFolderElement(data, divContent,divContainer) {
    divContainer.classList.add("file");
    // Crear el icono del archivo
    var folderIcon = document.createElement("div");
    folderIcon.classList.add("folder-icon");
    divContainer.appendChild(folderIcon);

    // Crear la etiqueta del archivo con el nombre que recibes del back-end
    var folderLabel = document.createElement("div");
    folderLabel.classList.add("folder-label");
    folderLabel.textContent = data["name"];
    folderLabel.onclick = function(){
        selectFolder(data["path"])
    }
    divContainer.appendChild(folderLabel);

    // Agregar el archivo al contenedor
    divContent.appendChild(divContainer);
}