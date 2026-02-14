// Menu.tsx
function Menu() {
  return (
    <div className="menu">
      {/* Recuerda que en JSX, los elementos <a href="#"> pueden usar Link de React Router si tienes routing. */}
      <a href="./screens/login">login</a>
      <a href="#">Aprender</a>
      <a href="#">Videos</a>
      <a href="#">Descuentos</a>
      <a href="#">cursos</a>
      <a href="#">Ayuda</a>
    </div>
  );
}

export default Menu;