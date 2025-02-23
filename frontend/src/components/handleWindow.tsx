import axios from 'axios';
import React, {useEffect, useState } from 'react';

import { useToken } from "./tokenContext";
import DraggableWindow from './draggableWindow';
import CreateFolderModal from './modalFolder'


interface FileItem {
    name: string;
    code: string;
    type: string;
    size: string;
    modified_at: number;
    created_at: number;
    path: string;
}


const HandleWindow: React.FC = () => {
  const {token} = useToken();
  const [path, setPath] = useState<string>("/");
  const [dataList, setDataList] = useState<FileItem[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado para abrir/cerrar el modal


  //Función para realizar la llamada a la API
  const fetchData = async (currentPath: string) => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_SERVER_URL}/data/${token}${currentPath}`
      );

      if (response.data) {
        console.log('API call successful');
        setDataList(response.data); 

      }
    } catch (error) {
      console.log('API call failed');
      console.error(error);
    }
  };

  const fetchDownload = async (filename: string) => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_SERVER_URL}/data/${token}${path}${filename}`, 
        {responseType: 'blob',}
      );

      // Verificar si la respuesta es exitosa
      if (!response.data) {
        throw new Error('Error al descargar el archivo');
      }

      const url = window.URL.createObjectURL(new Blob([response.data]));

      // Simular el clic en el enlace para iniciar la descarga
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename); // Nombre del archivo al descargar
      document.body.appendChild(link);

     // Simular el clic en el enlace para iniciar la descarga
     link.click();

      // Limpiar y eliminar el enlace temporal
      window.URL.revokeObjectURL(url);
      document.body.removeChild(link);

    } catch (error) {
      console.error('Error:', error);
    }

  };


  const fetchDeleteFile = async (filename: string) => {
    try {
      // Realizar la solicitud DELETE al servidor
      const response = await axios.delete(
        `${import.meta.env.VITE_SERVER_URL}/data/${token}${path}${filename}`
      );
  
      // Verificar si la respuesta es exitosa
      if (response.status === 200) {
        console.log('File deleted successfully');
        fetchData(path); // Actualizar la lista de archivos después de la eliminación
      } else {
        console.error('Error deleting file:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };



  useEffect(() => {
    fetchData(path);
  }, [path]); //


  useEffect(() => {
    setPath("/");
    fetchData(path);

  }, [token]); // 


  // Función para manejar el clic en una carpeta
  const handleFolderClick = (folderName: string) => {
    const newPath = `${path}${folderName}/`; // Concatenar el nombre de la carpeta al path actual
    setPath(newPath); // Actualizar el path
  };

  // Función para retroceder a la carpeta anterior
  const handleGoBack = () => {
      if (path === '/') return; 
      const newPath = path.split('/').slice(0, -2).join('/') + '/'; // Eliminar la última carpeta del path
      setPath(newPath);
    };


  // Función para manejar la subida del archivo
  const handleFileUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Evitar el envío por defecto del formulario

    const formData = new FormData();
    const fileInput = event.currentTarget.querySelector('input[type="file"]') as HTMLInputElement;

    if (fileInput && fileInput.files && fileInput.files[0]) {
      const file = fileInput.files[0];
      formData.append('upload_file', file); // Agregar el archivo al FormData

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_SERVER_URL}/data/${token}${path}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data', // Especificar el tipo de contenido
            },
          }
        );

        if (response.status === 200) {
          console.log('File uploaded successfully');
          fetchData(path); // Actualizar la lista de archivos después de la subida
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    } else {
      console.error('No file selected');
    }
  };


  const formatTimestamp = (timestamp:number) => {
    const date = new Date(timestamp * 1000); // Convertir a milisegundos
    return date.toLocaleString(); // Formatear la fecha
  };


  const handleCreateFolder = async (folderName: string) => {
    try {
      // Aquí haces la llamada a la API para crear la carpeta
      const response = await axios.post(`${import.meta.env.VITE_SERVER_URL}/data/${token}${path}${folderName}`);
  
      if (response.status === 200) {
        console.log('Carpeta creada con éxito');
        fetchData(path); // Actualizar la lista de archivos/carpetas
      }
    } catch (error) {
      console.error('Error al crear la carpeta:', error);
    }
  };
  

  return (
    <DraggableWindow id="window" 
    title="Window" 
    width="800px" 
    height="400px"
    >
        <div className="toolbar-path">
          <button className='primary-button' onClick={handleGoBack} disabled={path === '/'}> ← </button>
				  <button className="primary-button">{path}</button>
			  </div>
        
        <div className="toolbar">
          <form method="post" encType="multipart/form-data" onSubmit={handleFileUpload}>
            <label htmlFor="file-upload" className="primary-button">
            <input id="file-upload" type="file" name="file" /> Select file </label>
            <button type="submit" className="primary-button">Upload Files</button>
          </form>

          <div>
            {/* Botón para abrir el modal */}
            <button
              onClick={() => setIsModalOpen(true)}
              className="primary-button"
            >
              Folder
            </button>

            {/* Modal de creación de carpeta */}
            <CreateFolderModal
              isOpen={isModalOpen}
              onClose={() => setIsModalOpen(false)}
              onCreate={handleCreateFolder}
            />
          </div>





        </div>

        <div className='content'>
        {
          dataList && dataList.length > 0 ? (
            dataList.map((item, index) => (
              item.type === 'dir' ? ( // Si es una carpeta
                <div
                  className="box"
                  key={index}
                  onClick={() => handleFolderClick(item.name)}
                  style={{ cursor: 'pointer' }}>
                  <div className="folder-icon"></div>
                  <div className="folder-label">{item.name}</div>
                  <div className="file-modified-time">Modified: {formatTimestamp(item.modified_at)}</div>
                  <div className="file-access-time">Created: {formatTimestamp(item.created_at)}</div>
                  <div><button className="delete-icon" onClick={ () => fetchDeleteFile(item.name)}> DELETE </button></div>

                </div>
              ) : ( // Si es un archivo
                <div className="box" key={index}>
                  <div className="file-icon"></div>
                  {/* <div className="file-label"></div> */}
                  <div className="file-label" onClick={ () => fetchDownload(item.name) }>{item.name}</div>
                  <div className="file-size">size: {item.size}</div>
                  <div className="file-modified-time">Modified: {formatTimestamp(item.modified_at)} </div>
                  <div className="file-access-time">Created: { formatTimestamp(item.created_at)} </div>
                  <div>
                    <button className="delete-icon" onClick={ () => fetchDeleteFile(item.name)}> DELETE </button>
                  </div>
                  {/* <div className="file-path">path: {item.path}</div> */}
                </div>
              )
            ))
          ) : (
            <div className="empty-message">No data available</div>
          )
        }
        </div>
    </DraggableWindow>

  );
};

export default HandleWindow;