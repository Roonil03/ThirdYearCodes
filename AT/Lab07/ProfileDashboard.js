import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  ImageBackground,
  FlatList,
  TouchableOpacity,
  Alert
} from 'react-native';

const ProfileDashboard = () => {

  const profileDetails = [
    { id: '1', label: 'Name', value: 'John Doe' },
    { id: '2', label: 'Profession', value: 'Software Developer Developer' },
    { id: '3', label: 'Experience', value: '3 Years' },
    { id: '4', label: 'Location', value: 'Antarctica' },
    { id: '5', label: 'Email', value: 'john@doe.com' }
  ];

  return (
    <ImageBackground
      source={{ uri: 'https://images.unsplash.com/photo-1503264116251-35a269479413' }}
      style={styles.background}
      blurRadius={2}
    >
      <View style={styles.overlay}>

        {/* Profile Image */}
        <Image
          source={{ uri: 'https://randomuser.me/api/portraits/women/10.jpg' }}
          style={styles.profileImage}
        />

        {/* Title */}
        <Text style={styles.title}>Profile Dashboard</Text>

        {/* Professional Details List */}
        <View style={{ flexGrow: 1, width: '100%', maxHeight: 300 }}>
          <FlatList
            data={profileDetails}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <View style={styles.listItem}>
                <Text style={styles.label}>{item.label}:</Text>
                <Text style={styles.value}>{item.value}</Text>
              </View>
            )}
          />
        </View>

        {/* Edit Profile Button */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => Alert.alert("Edit Profile Clicked")}
        >
          <Text style={styles.buttonText}>Edit Profile</Text>
        </TouchableOpacity>

      </View>
    </ImageBackground>
  );
};

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: '100%',
    height: '100vh',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 20,
    justifyContent: 'center'
  },
  profileImage: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 3,
    borderColor: '#fff',
    marginBottom: 15
  },
  title: {
    fontSize: 22,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 20
  },
  listItem: {
    flexDirection: 'row',
    marginVertical: 5
  },
  label: {
    color: '#ddd',
    fontWeight: 'bold',
    width: 120
  },
  value: {
    color: '#fff'
  },
  button: {
    marginTop: 20,
    backgroundColor: '#1e90ff',
    paddingVertical: 10,
    paddingHorizontal: 25,
    borderRadius: 25
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold'
  }
});

export default ProfileDashboard;