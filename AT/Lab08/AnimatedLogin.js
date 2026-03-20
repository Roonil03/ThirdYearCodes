import React, { useEffect, useRef } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Animated, 
  Dimensions 
} from 'react-native';

const LoginAnimationLab = () => {
  // 1. Animation Values
  // Logo starts at -200 (off-screen top)
  const slideAnim = useRef(new Animated.Value(-200)).current;
  // Button scale starts at 1
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // 2. Logo Slide Down Animation
    Animated.timing(slideAnim, {
      toValue: 0,          // Slide to its natural position
      duration: 1000,
      useNativeDriver: true,
    }).start();

    // 3. Continuous Pulse Animation for Button
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,    // Scale up by 10%
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,      // Scale back to original
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  return (
    <View style={styles.container}>
      {/* Animated Logo */}
      <Animated.View style={[styles.logoContainer, { transform: [{ translateY: slideAnim }] }]}>
        <View style={styles.logoCircle}>
          <Text style={styles.logoText}>App</Text>
        </View>
      </Animated.View>

      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Username" placeholderTextColor="#999" />
        <TextInput style={styles.input} placeholder="Password" secureTextEntry placeholderTextColor="#999" />

        {/* Animated Pulsing Button */}
        <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>LOGIN</Text>
          </TouchableOpacity>
        </Animated.View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  logoContainer: {
    marginBottom: 50,
    alignItems: 'center',
  },
  logoCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#6200ee',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  },
  logoText: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  form: {
    width: '100%',
  },
  input: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 15,
    backgroundColor: '#f9f9f9',
  },
  button: {
    backgroundColor: '#6200ee',
    height: 55,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
    elevation: 3,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default LoginAnimationLab;