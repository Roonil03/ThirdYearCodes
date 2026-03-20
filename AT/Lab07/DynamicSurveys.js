import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Switch, 
  StyleSheet, 
  FlatList, 
  Modal, 
  ScrollView 
} from 'react-native';

// 1. JSON Data Array - Defines questions and their types
const SURVEY_DATA = [
  { id: 'q1', type: 'text', question: 'What is your name?' },
  { id: 'q2', type: 'radio', question: 'How satisfied are you?', options: [1, 2, 3, 4, 5] },
  { id: 'q3', type: 'switch', question: 'Would you use this app again?' },
  { id: 'q4', type: 'text', question: 'Any additional comments?' },
];

const DynamicSurvey = () => {
  // 2. State to store answers dynamically: { q1: 'Ravi', q2: 4, q3: true }
  const [answers, setAnswers] = useState({});
  const [showSummary, setShowSummary] = useState(false);

  const updateAnswer = (id, value) => {
    setAnswers(prev => ({ ...prev, [id]: value }));
  };

  const handleReset = () => {
    setAnswers({});
    setShowSummary(false);
  };

  // 3. Dynamic Renderer for Input Types
  const renderInput = (item) => {
    switch (item.type) {
      case 'text':
        return (
          <TextInput
            style={styles.input}
            placeholder="Type here..."
            value={answers[item.id] || ''}
            onChangeText={(val) => updateAnswer(item.id, val)}
          />
        );
      case 'switch':
        return (
          <View style={styles.switchRow}>
            <Text>{answers[item.id] ? "Yes" : "No"}</Text>
            <Switch
              value={!!answers[item.id]}
              onValueChange={(val) => updateAnswer(item.id, val)}
            />
          </View>
        );
      case 'radio':
        return (
          <View style={styles.radioRow}>
            {item.options.map(opt => (
              <TouchableOpacity 
                key={opt} 
                onPress={() => updateAnswer(item.id, opt)}
                style={[styles.radioBtn, answers[item.id] === opt && styles.radioActive]}
              >
                <Text style={answers[item.id] === opt ? styles.activeText : null}>{opt}</Text>
              </TouchableOpacity>
            ))}
          </View>
        );
      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>User Survey</Text>
      
      <FlatList
        data={SURVEY_DATA}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.questionCard}>
            <Text style={styles.questionText}>{item.question}</Text>
            {renderInput(item)}
          </View>
        )}
        ListFooterComponent={
          <TouchableOpacity style={styles.submitBtn} onPress={() => setShowSummary(true)}>
            <Text style={styles.submitText}>Submit Survey</Text>
          </TouchableOpacity>
        }
      />

      {/* 4. Final Summary Announcement Popup */}
      <Modal visible={showSummary} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Survey Summary</Text>
            <ScrollView style={styles.summaryList}>
              {SURVEY_DATA.map(q => (
                <View key={q.id} style={styles.summaryItem}>
                  <Text style={styles.summaryQ}>{q.question}</Text>
                  <Text style={styles.summaryA}>
                    Ans: {String(answers[q.id] ?? 'Not answered')}
                  </Text>
                </View>
              ))}
            </ScrollView>
            
            <TouchableOpacity style={styles.resetBtn} onPress={handleReset}>
              <Text style={styles.resetText}>Reset & Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f4f7f6', paddingTop: 50 },
  header: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  questionCard: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 15, elevation: 2 },
  questionText: { fontSize: 16, fontWeight: '600', marginBottom: 10 },
  input: { borderBottomWidth: 1, borderColor: '#ccc', padding: 8 },
  switchRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  radioRow: { flexDirection: 'row', justifyContent: 'space-around' },
  radioBtn: { padding: 10, borderWidth: 1, borderColor: '#3498db', borderRadius: 5, minWidth: 40, alignItems: 'center' },
  radioActive: { backgroundColor: '#3498db' },
  activeText: { color: '#fff', fontWeight: 'bold' },
  submitBtn: { backgroundColor: '#2ecc71', padding: 15, borderRadius: 10, marginTop: 10, marginBottom: 30 },
  submitText: { color: '#fff', textAlign: 'center', fontWeight: 'bold' },
  
  // Modal Styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { width: '90%', height: '70%', backgroundColor: '#fff', borderRadius: 20, padding: 20 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 15, textAlign: 'center' },
  summaryList: { flex: 1 },
  summaryItem: { paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: '#eee' },
  summaryQ: { fontWeight: 'bold', fontSize: 14 },
  summaryA: { color: '#3498db' },
  resetBtn: { backgroundColor: '#e74c3c', padding: 15, borderRadius: 10, marginTop: 20 },
  resetText: { color: '#fff', textAlign: 'center', fontWeight: 'bold' }
});

export default DynamicSurvey;