import axios from 'axios';
import React, { useState, useEffect, useRef } from 'react';
import { useToken } from "../tokenContext";
import DraggableWindow from '../draggableWindow';
import io from 'socket.io-client';


interface Notification {
  dir: string;
  message: string;
  path: string;
}


const LoginForm: React.FC= () => {
  const [username, setUsername] = useState('');
  const { token, setToken } = useToken();
  const [notify, setNotify] = useState<Notification[]>([]); // Estado para almacenar notificaciones como objetos JSON
  const socketRef = useRef<any>(null); // Referencia para almacenar la instancia de Socket.IO
  const [animateIcon, setAnimateIcon] = useState(false);

  useEffect( () => {
    // Inicializar Socket.IO solo una vez cuando el componente se monta
    socketRef.current = io(import.meta.env.VITE_SERVER_URL, {    
      reconnection: true, 
      reconnectionAttempts: 5, 
      reconnectionDelay: 1000, 
      });


    // Configurar listeners de Socket.IO
    socketRef.current.on('connect', () => {
      console.log('Connected to server');
      socketRef.current.emit("join", { code: token });
    });


    socketRef.current.on('connect_error', (error:any) => {
      console.error('Connection error:', error);
      if (error.message === 'Invalid session') {
        // Manejar sesión inválida
        console.log('Sesión inválida. Reconectando...');
      }
    });


    socketRef.current.on("files", (data: any) => {
      console.log(data);
    });

    socketRef.current.on("notify", (data: string) => {
      const parsedData: Notification = JSON.parse(data); // Convertir el string a JSON

      // Activar la animación
      setAnimateIcon(true);

      // Reiniciar la animación después de 2 segundos
      setTimeout(() => {
        setAnimateIcon(false);
      }, 2000); // Duración de la animación


      // Agregar la nueva notificación al estado
      setNotify(prevNotifications => {
          const newNotifications = [...prevNotifications, parsedData];

          if (newNotifications.length >= 2) {
            return newNotifications.slice(1) // Elimina el primer elemento (el más antiguo)
          }

          return newNotifications;
        });



    });


    // Limpiar la conexión cuando el componente se desmonta
    return () => {
          if (socketRef.current) {
            socketRef.current.disconnect();
          }
    }

  }, [token]); 


  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
        const response = await axios.post(import.meta.env.VITE_SERVER_URL + '/token/account', {
        email: username,
      }, 
      {
        headers: {
          "Content-Type": "application/json", // Indica que el cuerpo es JSON
        },
      }
    );
      if (response.data) {
        localStorage.setItem('token', response.data.code);
        setToken(response.data.code)
      }
    } catch (error) {
      console.log('Login failed');
    }
  };


  return (
    <DraggableWindow id="loginWindow" 
    title="Login" 
    width="400px" 
    height="400px"
    >
    <div className="content">

			<div className="folder">
				<div className="folder-icon">
					<div className="email-icon"></div>
			  </div>
        <form id = "loginForm" onSubmit={handleLogin}>
            <input
              className="folder-label"
              type="email"
              id="email"
              name="email"
              placeholder="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <button className="primary-button" type="submit">Login</button>
        </form>
			</div>
      <> {token && (  
      
      <div>
        
        <div className="folder">
          
        <div className="file-icon">
          <div className={`${animateIcon ? 'notification-icon' : 'notification-icon-off'}`}></div>
        </div>

          <div className="folder-label"> {token} </div>
          
      </div>

            {/* Mostrar notificaciones */}
            <div className="notifications">
              {notify.map((notification, index) => (
                
                <div key={index}>
                
                  <div className="folder"> 
                    <div className="folder-label"> {notification.message} </div>
                  </div>
                
                  <div className='folder'>
                    <div className="folder-label"> <span className='folder-label-underline'>Path:</span>  {notification.path} </div>
                  </div>

                </div>


              ))}
            </div>
      </div>


 

      )}</>
		</div>
    </DraggableWindow>


  );
};

export default LoginForm;