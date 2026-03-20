import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Switch, StyleSheet, Modal, Alert } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

// --- SCREEN 1: PERSONAL DETAILS ---
const PersonalDetails = ({ navigation }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleNext = () => {
    if (!name.trim() || !email.trim()) {
      Alert.alert("Required", "Please provide your name and email.");
      return;
    }
    navigation.navigate('Preferences', { name, email });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.stepTitle}>Step 1: Personal Details</Text>
      <TextInput style={styles.input} placeholder="Full Name" value={name} onChangeText={setName} />
      <TextInput style={styles.input} placeholder="Email" value={email} onChangeText={setEmail} keyboardType="email-address" />
      <TouchableOpacity style={styles.primaryBtn} onPress={handleNext}>
        <Text style={styles.btnText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );
};

// --- SCREEN 2: PREFERENCES ---
const Preferences = ({ navigation, route }) => {
  const { name, email } = route.params;
  const [newsletter, setNewsletter] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <View style={styles.container}>
      <Text style={styles.stepTitle}>Step 2: Preferences</Text>
      <View style={styles.switchRow}>
        <Text>Subscribe to Updates</Text>
        <Switch value={newsletter} onValueChange={setNewsletter} />
      </View>
      <View style={styles.switchRow}>
        <Text>Enable Dark Mode</Text>
        <Switch value={darkMode} onValueChange={setDarkMode} />
      </View>
      <TouchableOpacity 
        style={styles.primaryBtn} 
        onPress={() => navigation.navigate('Summary', { name, email, newsletter, darkMode })}
      >
        <Text style={styles.btnText}>Review Summary</Text>
      </TouchableOpacity>
    </View>
  );
};

// --- SCREEN 3: SUMMARY & ANNOUNCEMENT ---
const Summary = ({ route, navigation }) => {
  const { name, email, newsletter, darkMode } = route.params;
  const [showPopup, setShowPopup] = useState(false);

  const handleFinalSubmit = () => {
    setShowPopup(true); // Trigger the Announcement Popup
  };

  const closeAndReset = () => {
    setShowPopup(false);
    navigation.popToTop(); // Go back to start and clear fields
  };

  return (
    <View style={styles.container}>
      <Text style={styles.stepTitle}>Step 3: Review Info</Text>
      <View style={styles.card}>
        <Text style={styles.cardItem}>👤 {name}</Text>
        <Text style={styles.cardItem}>📧 {email}</Text>
        <Text style={styles.cardItem}>🔔 Newsletter: {newsletter ? "Enabled" : "Disabled"}</Text>
        <Text style={styles.cardItem}>🌙 Theme: {darkMode ? "Dark" : "Light"}</Text>
      </View>

      <TouchableOpacity style={styles.submitBtn} onPress={handleFinalSubmit}>
        <Text style={styles.btnText}>CONFIRM & SUBMIT</Text>
      </TouchableOpacity>

      {/* ANNOUNCEMENT POPUP (MODAL) */}
      <Modal visible={showPopup} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalEmoji}>✅</Text>
            <Text style={styles.modalHeader}>Registration Success!</Text>
            
            <View style={styles.summaryBox}>
              <Text style={styles.summaryTitle}>Submitted Profile:</Text>
              <Text>Name: {name}</Text>
              <Text>Email: {email}</Text>
              <Text>Updates: {newsletter ? "Yes" : "No"}</Text>
              <Text>Dark Mode: {darkMode ? "Active" : "Inactive"}</Text>
            </View>

            <TouchableOpacity style={styles.closeBtn} onPress={closeAndReset}>
              <Text style={styles.closeBtnText}>Done</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

// --- NAVIGATION CONFIG ---
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="PersonalDetails" component={PersonalDetails} options={{ title: 'User Info' }} />
        <Stack.Screen name="Preferences" component={Preferences} options={{ title: 'User Preferences' }} />
        <Stack.Screen name="Summary" component={Summary} options={{ title: 'Final Summary' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center', backgroundColor: '#fff' },
  stepTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 20, color: '#333' },
  input: { borderWidth: 1, borderColor: '#ddd', padding: 12, borderRadius: 8, marginBottom: 15 },
  switchRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 15, borderBottomWidth: 1, borderBottomColor: '#f0f0f0' },
  primaryBtn: { backgroundColor: '#2196F3', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 10 },
  submitBtn: { backgroundColor: '#4CAF50', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 20 },
  btnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  card: { backgroundColor: '#f9f9f9', padding: 20, borderRadius: 12, borderWidth: 1, borderColor: '#eee' },
  cardItem: { fontSize: 16, marginBottom: 8 },
  
  // Modal Styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { width: '80%', backgroundColor: '#fff', padding: 25, borderRadius: 20, alignItems: 'center' },
  modalEmoji: { fontSize: 50, marginBottom: 10 },
  modalHeader: { fontSize: 22, fontWeight: 'bold', marginBottom: 15 },
  summaryBox: { width: '100%', backgroundColor: '#f0f7ff', padding: 15, borderRadius: 10, marginBottom: 20 },
  summaryTitle: { fontWeight: 'bold', marginBottom: 5 },
  closeBtn: { backgroundColor: '#333', paddingVertical: 10, paddingHorizontal: 40, borderRadius: 25 },
  closeBtnText: { color: '#fff', fontWeight: 'bold' }
});