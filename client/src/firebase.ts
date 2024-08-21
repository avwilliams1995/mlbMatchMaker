// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAF764yobJVTahHc4u7gKCw5mbannoBIto",
  authDomain: "mlb-matchmaker.firebaseapp.com",
  projectId: "mlb-matchmaker",
  storageBucket: "mlb-matchmaker.appspot.com",
  messagingSenderId: "948340024958",
  appId: "1:948340024958:web:4a9ad0d094c11a2b7a5a2f",
  measurementId: "G-HKY6HE6Q55"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;