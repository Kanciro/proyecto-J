import React, { useState } from 'react';
import type { FormEvent } from 'react';
import { useAuth } from '../logic/useLogin';

const LoginForm: React.FC = () => {
    // Estado local para los campos del formulario
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Importar la lógica del hook
    const { isLoggedIn, error, login, logout } = useAuth();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            await login({ username, password });
        } catch (err) {
            // El hook ya maneja el estado de error, solo mostramos el console.error
            console.error("Fallo de login manejado:", err);
        } finally {
            setIsLoading(false);
        }
    };

    // Si el usuario está logueado, mostrar un mensaje de bienvenida y el botón de logout
    if (isLoggedIn) {
        return (
            <div className="login-container success">
                <h2>🎉 ¡Bienvenido! Has iniciado sesión.</h2>
                <button onClick={logout} className="logout-button">Cerrar Sesión</button>
            </div>
        );
    }

    // Si no está logueado, mostrar el formulario
    return (
        <div className="login-container">
            <h2>Iniciar Sesión</h2>
            <form onSubmit={handleSubmit} className="login-form">
                {/* Mostrar mensaje de error si existe */}
                {error && <p className="error-message">{error}</p>}

                <div className="form-group">
                    <label htmlFor="username">Usuario:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        disabled={isLoading}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password">Contraseña:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={isLoading}
                    />
                </div>

                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Cargando...' : 'Entrar'}
                </button>

                <p className="hint">
                    💡 **Tip:** Usa `user` como usuario y `pass` como contraseña para probar.
                </p>
            </form>
        </div>
    );
};

export default LoginForm;