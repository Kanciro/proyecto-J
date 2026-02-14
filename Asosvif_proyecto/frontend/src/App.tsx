// App.tsx
import './App.css';
import { useState } from 'react'; // Importamos useState

// 1. Importar el componente de Login y el Hook de lógica
import Login from './login'; 
import { useAuth } from './logic/useLogin';

// Importar tus componentes de la interfaz
import TopBar from './components/TopBar';
import Navbar from './components/Navbar';
import Menu from './components/Menu';
import Banner from './components/Banner'; 
import ProductSection from './components/ProductSection';

function App() {
  // Usamos el hook para saber si el usuario está logueado
  const { isLoggedIn } = useAuth();

  return (
    <>
      {/* SI NO ESTÁ LOGUEADO: Muestra solo el Login */}
      {!isLoggedIn ? (
        <Login />
      ) : (
        /* SI YA SE LOGUEÓ: Muestra toda la página principal */
        <>
          <TopBar />
          <Navbar />
          <Menu />
          <Banner />
          <ProductSection />
        </>
      )}
    </>
  );
}

export default App;