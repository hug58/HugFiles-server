import React, { useState, useRef, MouseEvent } from "react";


interface DraggableWindowProps {
  id: string; // ID único para la ventana
  title?: string;
  width?: number | string;
  height?: number | string;
  children: React.ReactNode; // Contenido de la ventana
}

const DraggableWindow: React.FC<DraggableWindowProps> = ({ 
  id, 
  children,
  width = "400px",
  height = "200px",
  title = "Window", 

}) => {

  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [offset, setOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const windowRef = useRef<HTMLDivElement>(null);
  
  // Maneja el inicio del arrastre
  const dragStart = (event: MouseEvent<HTMLDivElement>) => {
    setIsDragging(true);

    if (windowRef.current) {
      setOffset({
        x: event.clientX - windowRef.current.offsetLeft,
        y: event.clientY - windowRef.current.offsetTop,
      });
    }
  };


  // Maneja el final del arrastre
  const dragEnd = () => {
    setIsDragging(false);
  };

  // Maneja el movimiento durante el arrastre
  const drag = (event: MouseEvent<HTMLDivElement>) => {
    if (isDragging && windowRef.current) {
      const x = event.clientX - offset.x;
      const y = event.clientY - offset.y;
      windowRef.current.style.left = `${x}px`;
      windowRef.current.style.top = `${y}px`;
    }
  };


  return (
    <div
      id={id}
      ref={windowRef}
      style={{
        position: "fixed",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)",
        width: width,
        height: height,
        backgroundColor: "var(--color-grey)",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
        cursor: isDragging ? "grabbing" : "grab",
        overflowY: "auto", // Agregar barra de desplazamiento vertical
      }}


      onMouseDown={dragStart}
      onMouseUp={dragEnd}
      onMouseMove={drag}>


      <div style={{
          backgroundColor: "var(--color-toolbar-dark)",
          padding: "10px",
          cursor: "move",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center", 
          position: "sticky",
          top: 0,
          zIndex: 1, }}>
            
        <span className="title">{title}</span>

      </div>
      <div>{children}</div>
      
    </div>
  );
};

export default DraggableWindow;