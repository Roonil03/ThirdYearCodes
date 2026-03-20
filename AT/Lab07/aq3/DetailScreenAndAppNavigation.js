import React from 'react'; // Added React import
import { View, Text, StyleSheet } from 'react-native'; // Added missing UI imports
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ProductProvider } from './ProductContext';
import ProductList from './ProductList';

const Stack = createStackNavigator();

const DetailsScreen = ({ route }) => {
  // Check if params exist to avoid crashing
  const { product } = route.params || {};
  
  if (!product) {
    return (
      <View style={styles.center}>
        <Text>No Product Data Found</Text>
      </View>
    );
  }

  return (
    <View style={styles.detailsContainer}>
      <Text style={styles.detailTitle}>{product.title}</Text>
      <Text style={styles.detailPrice}>Price: ${product.price}</Text>
      <Text style={styles.detailCategory}>Category: {product.category}</Text>
      <Text style={styles.detailDesc}>
        This is a detailed description of the {product.title}. 
        It features the latest technology and premium build quality.
      </Text>
    </View>
  );
};

export default function App() {
  return (
    <ProductProvider>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="Products" component={ProductList} />
          <Stack.Screen name="Details" component={DetailsScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </ProductProvider>
  );
}

// Added Styles to ensure layout works correctly
const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  detailsContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20, backgroundColor: '#fff' },
  detailTitle: { fontSize: 30, fontWeight: 'bold' },
  detailPrice: { fontSize: 22, color: '#28a745', marginVertical: 10 },
  detailCategory: { fontSize: 16, color: '#666' },
  detailDesc: { textAlign: 'center', marginTop: 20, lineHeight: 22, color: '#444' }
});