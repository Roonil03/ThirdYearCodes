import React, { useState, useContext, useEffect } from 'react';
import { View, Text, FlatList, TextInput, TouchableOpacity, StyleSheet, RefreshControl } from 'react-native';
import { ProductContext } from './ProductContext';

const ProductList = ({ navigation }) => {
  const { products } = useContext(ProductContext);
  const [filteredData, setFilteredData] = useState(products);
  const [search, setSearch] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  // Search Logic
  const handleSearch = (text) => {
    setSearch(text);
    const filtered = products.filter(item => 
      item.title.toLowerCase().includes(text.toLowerCase())
    );
    setFilteredData(filtered);
  };

  // Sorting Logic
  const sortData = (type) => {
    const sorted = [...filteredData].sort((a, b) => 
      type === 'asc' ? a.price - b.price : b.price - a.price
    );
    setFilteredData(sorted);
  };

  // Pull-to-Refresh
  const onRefresh = () => {
    setRefreshing(true);
    setTimeout(() => {
      setSearch('');
      setFilteredData(products);
      setRefreshing(false);
    }, 1500);
  };

  return (
    <View style={styles.container}>
      <TextInput 
        style={styles.searchBar} 
        placeholder="Search products..." 
        value={search}
        onChangeText={handleSearch}
      />

      <View style={styles.sortRow}>
        <TouchableOpacity style={styles.sortBtn} onPress={() => sortData('asc')}>
          <Text>Price Low-High</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.sortBtn} onPress={() => sortData('desc')}>
          <Text>Price High-Low</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={filteredData}
        keyExtractor={item => item.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        renderItem={({ item }) => (
          <TouchableOpacity 
            style={styles.productCard} 
            onPress={() => navigation.navigate('Details', { product: item })}
          >
            <Text style={styles.productTitle}>{item.title}</Text>
            <Text style={styles.productPrice}>${item.price}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

// Styles for Product List
const styles = StyleSheet.create({
  container: { flex: 1, padding: 15, backgroundColor: '#f8f9fa' },
  searchBar: { backgroundColor: '#fff', padding: 12, borderRadius: 8, borderWidth: 1, borderColor: '#ddd', marginBottom: 10 },
  sortRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 15 },
  sortBtn: { backgroundColor: '#e9ecef', padding: 10, borderRadius: 5 },
  productCard: { backgroundColor: '#fff', padding: 20, borderRadius: 10, marginBottom: 10, elevation: 2 },
  productTitle: { fontSize: 18, fontWeight: 'bold' },
  productPrice: { color: '#28a745', fontSize: 16, marginTop: 5 }
});

export default ProductList;