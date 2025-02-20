import React, {useEffect, useState } from 'react';
import axios from 'axios';



const styles = {
    overlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)', // Fondo oscuro semi-transparente
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1000,
    },
    modal: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
      width: '300px',
      textAlign: 'center',
    },
    input: {
      width: '100%',
      padding: '10px',
      margin: '10px 0',
      borderRadius: '4px',
      border: '1px solid var(--color-grey)',
      fontSize: '16px',
    },
    buttonContainer: {
      display: 'flex',
      justifyContent: 'space-between',
      marginTop: '20px',
    },
    cancelButton: {
      backgroundColor: 'var(--color-delete)',
      color: 'white',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    createButton: {
      backgroundColor: 'var(--color-toolbar)',
      color: 'white',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '4px',
      cursor: 'pointer',
    },
  } as const;



  
const CreateFolderModal = ({ isOpen, onClose, onCreate }: {
    isOpen: boolean;
    onClose: () => void;
    onCreate: (folderName: string) => void;
  }) => {
    const [inputValue, setInputValue] = useState('');
  
    if (!isOpen) return null;
  
    const handleCreate = () => {
      onCreate(inputValue);
      setInputValue('');
      onClose();
    };
  
    return (
      <div style={styles.overlay}>
        <div style={styles.modal}>
          <h3>Create new folder</h3>
          <input
            type="text" 
            placeholder="Names's Folder"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            style={styles.input}
          />
          <div style={styles.buttonContainer}>
            <button onClick={onClose} style={styles.cancelButton}>
              EXIT
            </button>
            <button onClick={handleCreate} style={styles.createButton}>
              CREATE
            </button>
          </div>
        </div>
      </div>
    );
  };


export default CreateFolderModal;