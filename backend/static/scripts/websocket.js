function done(idFile,data){
    const modified_at = data["modified_at"] ?? 0;
    const created_at = data["created_at"] ?? 0;
    const type = data["type"] ?? "file";

    // Obtener el contenedor de los archivos
    var fileContainer = document.querySelector(".content");

    // Crear el elemento del archivo
    var file = document.createElement("div");
    if (type == "file") {
        file.classList.add("file");

        // Crear el icono del archivo
        var fileIcon = document.createElement("div");
        fileIcon.classList.add("file-icon");
        file.appendChild(fileIcon);
    
        // Crear la etiqueta del archivo con el nombre que recibes del back-end
        var fileLabel = document.createElement("div");
        fileLabel.classList.add("file-label");
        fileLabel.textContent = data["name"];
        file.appendChild(fileLabel);
    
        // Crear la etiqueta de tamaño del archivo con el tamaño que recibes del back-end
        var fileSize = document.createElement("div");
        fileSize.classList.add("file-size");
        fileSize.textContent ="Size: " +  bytesToMB(data["size"]) + " MB";
        file.appendChild(fileSize);
    
        // Crear la etiqueta de tiempo modificado del archivo con la fecha que recibes del back-end
        var fileModifiedTime = document.createElement("div");
        fileModifiedTime.classList.add("file-modified-time");
        fileModifiedTime.textContent = "Modified At: " + unixTimestampToDateString(modified_at);

        file.appendChild(fileModifiedTime);
        // Crear la etiqueta de tiempo de acceso del archivo con la fecha que recibes del back-end
        var fileAccessTime = document.createElement("div");
        fileAccessTime.classList.add("file-access-time");
        fileAccessTime.textContent =  "Accessed At:" +  unixTimestampToDateString(created_at);
        file.appendChild(fileAccessTime);
        
        // Crear la etiqueta de ruta del archivo con la ruta que recibes del back-end
        var filePath = document.createElement("div");
        filePath.classList.add("file-path");
        filePath.textContent = "Path: " +  data["path"];
        file.appendChild(filePath);
    
        // Agregar el archivo al contenedor
        fileContainer.appendChild(file);
    } else {
        createFolderElement(data, fileContainer,file)
    }
   
}




let id = 0;
console.log("starting on files")

socket.on('files',function(files){
    console.log("recevied data")

    files = JSON.parse(files);
    id ++;
    console.log(files)
    done(id,files);

    // if(files['status'] || files['created']){
    //     id ++;
    //     console.log(id)
    // }
});


socket.on('notify',function(data){
    data = JSON.parse(data);
    console.log(data);

});

