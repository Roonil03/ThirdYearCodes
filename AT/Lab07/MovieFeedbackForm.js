import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Switch, 
  StyleSheet, 
  Modal,
  ScrollView 
} from 'react-native';

const App = () => {
  // Form States
  const [movieName, setMovieName] = useState('');
  const [rating, setRating] = useState(0);
  const [isRecommended, setIsRecommended] = useState(false);
  
  // UI State for the Announcement Popup
  const [modalVisible, setModalVisible] = useState(false);

  const handleSubmit = () => {
    if (movieName.trim() === "" || rating === 0) {
      alert("Please fill in all fields!"); // Simple fallback validation
      return;
    }
    // Show the announcement popup
    setModalVisible(true);
  };

  const closeAndReset = () => {
    // Hide popup
    setModalVisible(false);
    // Clear all fields for a new form
    setMovieName('');
    setRating(0);
    setIsRecommended(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Movie Feedback Form</Text>

      {/* Input Section */}
      <Text style={styles.label}>Movie Name:</Text>
      <TextInput
        style={styles.input}
        placeholder="e.g. Inception"
        value={movieName}
        onChangeText={setMovieName}
      />

      {/* Star Rating Section */}
      <Text style={styles.label}>Rating (1-5 Stars):</Text>
      <View style={styles.radioRow}>
        {[1, 2, 3, 4, 5].map((num) => (
          <TouchableOpacity 
            key={num} 
            onPress={() => setRating(num)} 
            style={styles.radioItem}
          >
            <View style={[styles.circle, rating === num && styles.selectedCircle]} />
            <Text style={styles.radioText}>{num}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Switch Section */}
      <View style={styles.switchRow}>
        <Text style={styles.label}>Would you recommend this?</Text>
        <Switch 
          value={isRecommended} 
          onValueChange={setIsRecommended}
          trackColor={{ false: "#767577", true: "#81b0ff" }}
        />
      </View>

      {/* Submit Button */}
      <TouchableOpacity style={styles.submitBtn} onPress={handleSubmit}>
        <Text style={styles.submitBtnText}>SUBMIT FEEDBACK</Text>
      </TouchableOpacity>

      {/* --- ANNOUNCEMENT MODAL --- */}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalView}>
            <Text style={styles.modalHeader}>Form Submitted!</Text>
            
            <View style={styles.detailsContainer}>
              <Text style={styles.detailText}>Movie: {movieName}</Text>
              <Text style={styles.detailText}>Rating: {rating} / 5</Text>
              <Text style={styles.detailText}>Recommend: {isRecommended ? "Yes" : "No"}</Text>
            </View>

            <Text style={styles.saveNote}>Data synchronized to data.json</Text>

            <TouchableOpacity style={styles.closeBtn} onPress={closeAndReset}>
              <Text style={styles.closeBtnText}>New Feedback</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 30, justifyContent: 'center', backgroundColor: '#fff' },
  header: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 30, color: '#2c3e50' },
  label: { fontSize: 16, marginTop: 20, color: '#34495e', fontWeight: '500' },
  input: { borderBottomWidth: 2, borderColor: '#3498db', padding: 10, fontSize: 16, marginTop: 5 },
  
  // Radio Styles
  radioRow: { flexDirection: 'row', justifyContent: 'space-around', marginTop: 15 },
  radioItem: { alignItems: 'center' },
  circle: { height: 24, width: 24, borderRadius: 12, borderWidth: 2, borderColor: '#3498db' },
  selectedCircle: { backgroundColor: '#3498db' },
  radioText: { marginTop: 5, fontWeight: 'bold' },

  // Switch Styles
  switchRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 30 },
  
  // Button Styles
  submitBtn: { backgroundColor: '#2ecc71', padding: 15, borderRadius: 10, marginTop: 40 },
  submitBtnText: { color: '#fff', textAlign: 'center', fontWeight: 'bold', fontSize: 18 },

  // Modal Styles
  modalOverlay: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.5)' },
  modalView: { width: '85%', backgroundColor: 'white', borderRadius: 20, padding: 25, alignItems: 'center', elevation: 5 },
  modalHeader: { fontSize: 22, fontWeight: 'bold', color: '#2ecc71', marginBottom: 15 },
  detailsContainer: { width: '100%', backgroundColor: '#f9f9f9', padding: 15, borderRadius: 10, marginBottom: 15 },
  detailText: { fontSize: 16, marginVertical: 5, color: '#2c3e50' },
  saveNote: { fontSize: 12, color: '#7f8c8d', fontStyle: 'italic', marginBottom: 20 },
  closeBtn: { backgroundColor: '#3498db', paddingHorizontal: 30, paddingVertical: 10, borderRadius: 5 },
  closeBtnText: { color: '#fff', fontWeight: 'bold' }
});

export default App;