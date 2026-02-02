# Lab Exercises:

1. Write a Flutter program to demonstrate basic property animation using AnimatedContainer:
   - Create a square Container of size 100×100.
   - On button tap:
     - Toggle the container color between blue and red.
     - Toggle the container size between 100 and 200.
   - Use AnimatedContainer with:
     - Duration: 1 second
     - Curve: Curves.easeInOut

2. Write a Flutter program to create a shape-morphing card animation:
   - Initially align the card to the left.
   - On tap:
     - Move the card to the right.
     - Animate the border radius from 0 to 30.
     - Add or remove a shadow.
   - Bonus: Animate margin or padding for smoother transition.

3. Write a Flutter program to demonstrate opacity animation using AnimatedOpacity:
   - Display a text: “Welcome to Flutter Animations”.
   - A button should toggle the text opacity between 0.0 and 1.0.
   - Duration of animation: 800 milliseconds.
   - Note: The widget should not be removed, only faded.

4. Write a Flutter program to reveal an image using opacity animation:
   - Display a placeholder icon initially.
   - On button press:
     - Fade in an image.
     - Fade out the placeholder icon.
   - Hint: Use Stack with two AnimatedOpacity widgets.

5. Write a Flutter program to demonstrate AnimatedCrossFade:
   - Create two widgets:
     - A login button.
     - A user profile card.
   - On button tap, crossfade between the two widgets.
   - Use:
     - AnimatedCrossFade
     - Duration: 1 second
     - CrossFadeState.showFirst and CrossFadeState.showSecond

6. Write a Flutter program to create an expandable FAQ tile:
   - First view shows only the question.
   - Second view shows both question and answer.
   - Tapping the tile toggles between compact and expanded views.
   - Bonus: Combine with AnimatedSize for smoother expansion.

7. Write a Flutter program to create a pulsing circle using AnimationController:
   - The circle should continuously grow and shrink.
   - Scale range: 0.8 to 1.2.
   - The animation should loop continuously.
   - Use:
     - SingleTickerProviderStateMixin
     - AnimationController
     - Tween<double>

8. Write a Flutter program to rotate an icon on button press:
   - Display a refresh icon.
   - On button press:
     - Rotate the icon 360 degrees.
     - Stop after one full rotation.
   - Hint: Use AnimatedBuilder or RotationTransition.

9. Write a Flutter program to create a custom fade and slide animation:
   - A widget should enter the screen from the bottom.
   - At the same time:
     - Fade in.
     - Slide upward.
   - Use:
     - One AnimationController
     - Two Tweens (Offset and double for opacity).


# Additional Exercises:

1. Write a Flutter program to create an animated theme switcher:
    - Toggle between Light mode and Dark mode.
    - Animate:
      - Background color using AnimatedContainer.
      - Icon opacity using AnimatedOpacity.
      - Icon rotation using AnimationController.
    - The final output should feel like a smooth, real-app UI transition.