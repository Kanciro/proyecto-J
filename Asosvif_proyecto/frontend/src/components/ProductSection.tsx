// src/components/ProductSection.tsx
import ProductCard from './ProductCard'; 
import { productData } from '../Data/ProductData'; 
// Importamos los datos (asumiendo que están disponibles aquí)

function ProductSection() {
  return (
    <div className="section">
      {/* 1. Tomamos el array de datos (productData).
        2. Llamamos a .map(). Por cada elemento (product) en el array, 
           hace algo y devuelve el resultado.
        3. Lo que devuelve .map() es un componente <ProductCard />.
      */}
      {productData.map((product) => (
        <ProductCard
          // **KEY:** Es crucial. React la usa para rastrear cada elemento. Debe ser única (usamos product.id).
          key={product.id} 
          
          // **PROPS:** Aquí "conectamos" los datos del objeto 'product' 
          // con los "espacios en blanco" que espera ProductCard
          image={product.image}
          title={product.title}
          description={product.description}
          buttonText={product.buttonText}
        />
      ))}
    </div>
  );
}

export default ProductSection;
