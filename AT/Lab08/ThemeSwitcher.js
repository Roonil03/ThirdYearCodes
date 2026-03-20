import React, { useState, useEffect } from 'react';
import { View, Text, Switch, StyleSheet, SafeAreaView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const ThemeSwitcherLab = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Load the stored theme preference when the component mounts
  useEffect(() => {
    loadTheme();
  }, []);

  // Save the theme preference to AsyncStorage
  const saveTheme = async (value) => {
    try {
      // AsyncStorage only stores strings, so we convert boolean to string
      await AsyncStorage.setItem('@theme_mode', JSON.stringify(value));
      setIsDarkMode(value);
    } catch (e) {
      console.log("Error saving theme preference");
    }
  };

  // Retrieve the theme preference from AsyncStorage
  const loadTheme = async () => {
    try {
      const val = await AsyncStorage.getItem('@theme_mode');
      if (val !== null) {
        setIsDarkMode(JSON.parse(val));
      }
    } catch (e) {
      console.log("Error loading theme preference");
    }
  };

  // Define dynamic styles based on the current theme
  const themeStyles = {
    backgroundColor: isDarkMode ? '#222' : '#fff',
    textColor: isDarkMode ? '#fff' : '#000',
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: themeStyles.backgroundColor }]}>
      <View style={styles.content}>
        <Text style={[styles.title, { color: themeStyles.textColor }]}>
          {isDarkMode ? 'Dark Mode Active' : 'Light Mode Active'}
        </Text>
        
        <View style={styles.row}>
          <Text style={{ color: themeStyles.textColor, fontSize: 18, marginRight: 10 }}>
            Switch Theme:
          </Text>
          <Switch
            value={isDarkMode}
            onValueChange={(value) => saveTheme(value)}
            trackColor={{ false: "#767577", true: "#81b0ff" }}
            thumbColor={isDarkMode ? "#f5dd4b" : "#f4f3f4"}
          />
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
});

export default ThemeSwitcherLab;