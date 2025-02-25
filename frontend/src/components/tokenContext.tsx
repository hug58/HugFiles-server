import React, { createContext, useState, useContext } from "react";

// Crear el contexto
interface TokenContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

const TokenContext = createContext<TokenContextType | undefined>(undefined);

// Hook personalizado para usar el contexto
export const useToken = () => {
  const context = useContext(TokenContext);
  if (!context) {
    throw new Error("useToken debe usarse dentro de un TokenProvider");
  }
  return context;
};

// Proveedor del contexto
export const TokenProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  return (
    <TokenContext.Provider value={{ token, setToken }}>
      {children}
    </TokenContext.Provider>
  );
};