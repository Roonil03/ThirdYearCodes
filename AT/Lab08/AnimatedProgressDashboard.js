import React, { useState, useEffect, useRef } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  Animated, 
  TouchableOpacity, 
  ActivityIndicator 
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const ProgressDashboard = () => {
  const [progressValue, setProgressValue] = useState(0);
  const [loading, setLoading] = useState(false);
  
  // Animated value for the bar width
  const animatedWidth = useRef(new Animated.Value(0)).current;

  // Load saved progress on mount
  useEffect(() => {
    const loadProgress = async () => {
      try {
        const savedValue = await AsyncStorage.getItem('@dashboard_progress');
        if (savedValue !== null) {
          const parsedValue = parseInt(savedValue);
          setProgressValue(parsedValue);
          triggerAnimation(parsedValue);
        }
      } catch (e) {
        console.error("Failed to load progress");
      }
    };
    loadProgress();
  }, []);

  const triggerAnimation = (toValue) => {
    Animated.timing(animatedWidth, {
      toValue: toValue, // 0 to 100
      duration: 1000,
      useNativeDriver: false, // width is not supported by native driver
    }).start();
  };

  const handleSync = async () => {
    setLoading(true);
    
    // Simulate network delay
    setTimeout(async () => {
      const newProgress = Math.floor(Math.random() * 100) + 1; // Random progress 1-100
      
      try {
        await AsyncStorage.setItem('@dashboard_progress', newProgress.toString());
        setProgressValue(newProgress);
        triggerAnimation(newProgress);
      } catch (e) {
        console.error("Failed to save progress");
      } finally {
        setLoading(false);
      }
    }, 2000);
  };

  // Interpolate numerical value to percentage for style
  const barWidth = animatedWidth.interpolate({
    inputRange: [0, 100],
    outputRange: ['0%', '100%']
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Progress Dashboard</Text>
      
      <View style={styles.card}>
        <Text style={styles.label}>Goal Completion: {progressValue}%</Text>
        
        {/* Progress Bar Container */}
        <View style={styles.progressBarBackground}>
          {/* Animated Fill */}
          <Animated.View style={[styles.progressBarFill, { width: barWidth }]} />
        </View>

        <TouchableOpacity 
          style={styles.syncButton} 
          onPress={handleSync}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Sync Data</Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f2f5', justifyContent: 'center', padding: 20 },
  title: { fontSize: 26, fontWeight: 'bold', textAlign: 'center', marginBottom: 30, color: '#1a1a1a' },
  card: { backgroundColor: '#fff', padding: 25, borderRadius: 15, elevation: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 8 },
  label: { fontSize: 18, marginBottom: 15, fontWeight: '600', color: '#444' },
  progressBarBackground: { height: 20, backgroundColor: '#e0e0e0', borderRadius: 10, overflow: 'hidden', marginBottom: 25 },
  progressBarFill: { height: '100%', backgroundColor: '#6200ee' },
  syncButton: { backgroundColor: '#6200ee', padding: 15, borderRadius: 10, alignItems: 'center', height: 55, justifyContent: 'center' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' }
});

export default ProgressDashboard;