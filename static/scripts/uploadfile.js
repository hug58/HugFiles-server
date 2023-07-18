function showFileInput() {
    const inputContainer = document.createElement('div');
    inputContainer.classList.add('input-container');
    inputContainer.innerHTML = `
      <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="archivo">
        <button type="submit">Subir archivo</button>
        <button type="button" onclick="closeInput()">Cancelar</button>
      </form>
    `;
    document.body.appendChild(inputContainer);
  }
  
  function closeInput() {
    const inputContainer = document.querySelector('.input-container');
    inputContainer.remove();
  }