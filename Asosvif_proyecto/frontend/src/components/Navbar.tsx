// Navbar.tsx
function Navbar() {
  return (
    <div className="navbar">
      <div className="logo">🌱 Mundo Hidroponía</div>
      <input type="text" placeholder="Buscar producto..." />
      <div className="actions">
        <span>Acceder</span>
        <span>❤ Favoritos</span>
        <span>🛒 Carrito</span>
      </div>
    </div>
  );
}

export default Navbar;