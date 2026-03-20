import React, { createContext, useState } from 'react';

export const ProductContext = createContext();

export const ProductProvider = ({ children }) => {
  const [products, setProducts] = useState([
    { id: '1', title: 'iPhone 15', price: 999, category: 'Tech' },
    { id: '2', title: 'MacBook Air', price: 1200, category: 'Tech' },
    { id: '3', title: 'Nike Shoes', price: 120, category: 'Fashion' },
    { id: '4', title: 'Coffee Maker', price: 85, category: 'Home' },
    { id: '5', title: 'Gaming Chair', price: 250, category: 'Office' },
  ]);

  return (
    <ProductContext.Provider value={{ products, setProducts }}>
      {children}
    </ProductContext.Provider>
  );
};