import React, { createContext, useState, useContext} from 'react';

interface WindowsContextType {
  windows: string[] ;
  setWindows: (token: string[]) => void;
}

const WindowsContext = createContext<WindowsContextType | undefined>(undefined);

// Hook personalizado para usar el contexto
export const useWindow = () => {
  const context = useContext(WindowsContext);
  if (!context) {
    throw new Error("useWindow debe usarse dentro de un WindowsProvider");
  }
  return context;
};


// Proveedor del contexto
export const WindowsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [windows, setWindows] = useState<string[]>([]);

  return (
    <WindowsContext.Provider value={{ windows, setWindows }}>
      {children}
    </WindowsContext.Provider>
  );
};


