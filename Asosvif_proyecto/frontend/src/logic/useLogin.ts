import { useState, useCallback } from 'react';

// 1. Ajustamos la interfaz para que use 'email' en lugar de 'username'
interface Credentials {
  email: string;
  password: string;
}

interface AuthHook {
  isLoggedIn: boolean;
  error: string | null;
  loading: boolean; // Añadimos estado de carga
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const useAuth = (): AuthHook => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const login = useCallback(async ({ email, password }: Credentials) => {
    setError(null);
    setLoading(true);

    try {
      // 2. CONEXIÓN REAL AL BACKEND
      const response = await fetch('http://127.0.0.1:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Si el backend responde con error (401, 404, etc.)
        throw new Error(data.detail || 'Error en el inicio de sesión');
      }

      // 3. SI TODO SALE BIEN
      console.log('Respuesta del servidor:', data);
      setIsLoggedIn(true);
      
      // Opcional: Guardar datos en el navegador para que no se borren al refrescar
      localStorage.setItem('userToken', data.user.id);
      localStorage.setItem('userRole', data.user.rol);

    } catch (err: any) {
      setError(err.message);
      setIsLoggedIn(false);
      throw err; // Re-lanzamos para que el componente Login.tsx sepa que falló
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setIsLoggedIn(false);
    setError(null);
    localStorage.clear();
    console.log('Sesión cerrada.');
  }, []);

  return {
    isLoggedIn,
    error,
    loading,
    login,
    logout,
  };
};