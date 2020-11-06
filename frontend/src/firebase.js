import firebase from 'firebase/app'
import 'firebase/firestore';

const firebaseConfig = firebase.initializeApp({
    apiKey: "AIzaSyAXF3E7hzdxDTWVlESEt6IzTjAAJmrB8SE",
    authDomain: "todoist-f1762.firebaseapp.com",
    databaseURL: "https://todoist-f1762.firebaseio.com",
    projectId: "todoist-f1762",
    storageBucket: "todoist-f1762.appspot.com",
    messagingSenderId: "229473655997",
    appId: "1:229473655997:web:09ed3b2ce2e1f65797abd4"
});

export {firebaseConfig as firebase};