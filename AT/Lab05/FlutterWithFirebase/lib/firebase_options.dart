import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      return const FirebaseOptions(
        apiKey: "AIzaSyDPPCu8DSV40WDCmyT25jpB8GnLOo18hfc",
        authDomain: "student-app-ae494.firebaseapp.com",
        projectId: "student-app-ae494",
        storageBucket: "student-app-ae494.firebasestorage.app",
        messagingSenderId: "338112694738",
        appId: "1:338112694738:web:21c6a2c8448884f89d200b",
        measurementId: "G-58N0CQ8SYZ",
      );
    }

    throw UnsupportedError(
      'DefaultFirebaseOptions are not supported for this platform.',
    );
  }
}
