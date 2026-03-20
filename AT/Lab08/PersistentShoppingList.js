import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  StyleSheet, 
  Alert 
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const ShoppingListApp = () => {
  const [item, setItem] = useState('');
  const [list, setList] = useState([]);

  // Load data from local database on startup
  useEffect(() => {
    loadList();
  }, []);

  const saveList = async (newList) => {
    try {
      // Convert array to string for storage
      const jsonValue = JSON.stringify(newList);
      await AsyncStorage.setItem('@shopping_list', jsonValue);
    } catch (e) {
      console.log("Error saving list");
    }
  };

  const loadList = async () => {
    try {
      const jsonValue = await AsyncStorage.getItem('@shopping_list');
      // Parse string back to array if data exists
      if (jsonValue !== null) {
        setList(JSON.parse(jsonValue));
      }
    } catch (e) {
      console.log("Error loading list");
    }
  };

  const addItem = () => {
    if (item.trim() === '') {
      Alert.alert("Error", "Item name cannot be empty");
      return;
    }
    const newList = [...list, { id: Date.now().toString(), name: item }];
    setList(newList);
    saveList(newList);
    setItem(''); // Clear input field
  };

  const deleteItem = (id) => {
    const newList = list.filter(listItem => listItem.id !== id);
    setList(newList);
    saveList(newList);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🛒 My Shopping List</Text>
      
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Add new item..."
          value={item}
          onChangeText={setItem}
        />
        <TouchableOpacity style={styles.addButton} onPress={addItem}>
          <Text style={styles.addButtonText}>Add</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={list}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.listItem}>
            <Text style={styles.itemText}>{item.name}</Text>
            <TouchableOpacity 
              onPress={() => deleteItem(item.id)}
              style={styles.deleteButton}
            >
              <Text style={styles.deleteButtonText}>Delete</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, paddingTop: 60, backgroundColor: '#fdfdfd' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  inputContainer: { flexDirection: 'row', marginBottom: 20 },
  input: { 
    flex: 1, 
    borderWidth: 1, 
    borderColor: '#ddd', 
    padding: 10, 
    borderRadius: 5, 
    backgroundColor: '#fff' 
  },
  addButton: { 
    backgroundColor: '#4CAF50', 
    padding: 10, 
    marginLeft: 10, 
    borderRadius: 5, 
    justifyContent: 'center' 
  },
  addButtonText: { color: 'white', fontWeight: 'bold' },
  listItem: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    padding: 15, 
    backgroundColor: '#fff', 
    marginBottom: 10, 
    borderRadius: 8,
    elevation: 2, // Shadow for Android
    shadowColor: '#000', // Shadow for iOS
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  itemText: { fontSize: 18 },
  deleteButton: { backgroundColor: '#ff5252', padding: 8, borderRadius: 5 },
  deleteButtonText: { color: 'white', fontSize: 12, fontWeight: 'bold' }
});

export default ShoppingListApp;