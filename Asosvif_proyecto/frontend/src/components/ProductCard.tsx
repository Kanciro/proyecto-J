// src/components/ProductCard.tsx

// Estas son las "entradas" o props que ProductCard espera recibir
interface ProductCardProps {
  image: string;
  title: string;
  description: string;
  buttonText: string;
}

// El componente recibe las entradas y las usa en el HTML (JSX)
function ProductCard({ image, title, description, buttonText }: ProductCardProps) {
  return (
    <div className="card">
      {/* Las llaves {} le dicen a React que inserte una variable */}
      <img src={image} alt={title} />
      <h3>{title}</h3>
      <p>{description}</p>
      <a href="#" className="btn">{buttonText}</a>
    </div>
  );
}

export default ProductCard;