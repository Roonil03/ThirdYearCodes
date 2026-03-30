# Lab Exercises
1. Animated Login Transition
    - Design a login screen where the logo slides down from the top.
    - The "Login" button should pulse (scale up and down) continuously using Animated.loop.
2. Persistent Shopping List
    - Create an app to add items to a list using a TextInput.
    - Store the entire array of items in AsyncStorage (Hint: Use JSON.stringify and JSON.parse).
    - Display items using FlatList with a delete button for each item.
3. Theme Switcher (Light/Dark Mode)
    - Implement a Switch component to toggle themes.
    - Store the theme preference in the local database so it persists even if the app is closed.
    - Use the stored value to set the background and text color on app start.
# Additional Exercise
1. Animated Progress Dashboard:
    - Create a progress bar that animates its width from 0% to X% based on data fetched from AsyncStorage.
    - Add a "Sync" button that simulates a network delay (using setTimeout) before updating the local storage and triggering the bar animation.