import React, { useState } from 'react';
import { 
  View, 
  Text, 
  FlatList, 
  TouchableOpacity, 
  StyleSheet, 
  Dimensions, 
  Modal 
} from 'react-native';

// Sample Category Data
const CATEGORIES = [
  { id: '1', title: 'Action', icon: '🎬', color: '#ff5e57' },
  { id: '2', title: 'Comedy', icon: '😂', color: '#ffdd59' },
  { id: '3', title: 'Drama', icon: '🎭', color: '#485460' },
  { id: '4', title: 'Horror', icon: '👻', color: '#05c46b' },
  { id: '5', title: 'Sci-Fi', icon: '🚀', color: '#00d8d6' },
  { id: '6', title: 'Romance', icon: '💖', color: '#ef5777' },
];

const App = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const handlePress = (item) => {
    setSelectedCategory(item);
    setModalVisible(true);
  };

  const renderCard = ({ item }) => (
    <TouchableOpacity 
      style={[styles.card, { borderLeftColor: item.color }]} 
      onPress={() => handlePress(item)}
    >
      <Text style={styles.icon}>{item.icon}</Text>
      <Text style={styles.cardTitle}>{item.title}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Movie Categories</Text>
      
      <FlatList
        data={CATEGORIES}
        renderItem={renderCard}
        keyExtractor={item => item.id}
        numColumns={2} // This creates the grid
        columnWrapperStyle={styles.row} // Spacing between columns
        contentContainerStyle={styles.listPadding}
      />

      {/* Announcement Popup */}
      <Modal
        transparent={true}
        visible={modalVisible}
        animationType="fade"
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalView}>
            <Text style={styles.modalEmoji}>{selectedCategory?.icon}</Text>
            <Text style={styles.modalText}>You explored the</Text>
            <Text style={styles.categoryName}>{selectedCategory?.title} Section</Text>
            
            <TouchableOpacity 
              style={styles.closeBtn} 
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.closeBtnText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f2f5', paddingTop: 50 },
  header: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
  listPadding: { paddingHorizontal: 10 },
  row: { justifyContent: 'space-between' },
  
  // Card Style
  card: {
    backgroundColor: '#fff',
    flex: 1,
    margin: 10,
    height: 120,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    borderLeftWidth: 5,
    // Shadow for iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
    // Elevation for Android
    elevation: 4,
  },
  icon: { fontSize: 40, marginBottom: 10 },
  cardTitle: { fontSize: 16, fontWeight: '600', color: '#333' },

  // Modal Styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', alignItems: 'center' },
  modalView: { width: 280, backgroundColor: '#fff', borderRadius: 20, padding: 30, alignItems: 'center' },
  modalEmoji: { fontSize: 60, marginBottom: 10 },
  modalText: { fontSize: 16, color: '#666' },
  categoryName: { fontSize: 22, fontWeight: 'bold', color: '#333', marginBottom: 20 },
  closeBtn: { backgroundColor: '#333', paddingVertical: 10, paddingHorizontal: 30, borderRadius: 25 },
  closeBtnText: { color: '#fff', fontWeight: 'bold' }
});

export default App;