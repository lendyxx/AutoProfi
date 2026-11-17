
import { initializeApp } from "https://www.gstatic.com/firebasejs/13.3.0/firebase-app.js";

import {
    getAuth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    updateProfile,
    signOut
} from "https://www.gstatic.com/firebasejs/13.3.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyCD2I3zjqYiVabBH8P_FpQqt2S0TJGoBgY",
    authDomain: "autoprofi-service.firebaseapp.com",
    projectId: "autoprofi-service",
    storageBucket: "autoprofi-service.firebasestorage.app",
    messagingSenderId: "904731124567",
    appId: "1:904731124567:web:378b99e0f97483297e9412",
    measurementId: "G-4DBHV4NFEF"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    updateProfile,
    signOut
};
