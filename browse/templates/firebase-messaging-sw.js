// [START initialize_firebase_in_sw]
// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts("https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js");

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
// const firebaseConfig = {
// 	apiKey: "AIzaSyBbzToDMnh5748JZ1-Z5YVMw-6yZxM3vAY",
// 	authDomain: "test-eb006.firebaseapp.com",
// 	databaseURL: "https://test-eb006-default-rtdb.firebaseio.com",
// 	projectId: "test-eb006",
// 	storageBucket: "test-eb006.appspot.com",
// 	messagingSenderId: "456393506172",
// 	appId: "1:456393506172:web:7a7d7f3a1ccc8b26f9b8f9",
// 	measurementId: "G-FNRCK1FSHC",
//   };


// firebase.initializeApp(firebaseConfig);
firebase.initializeApp({
	// Replace messagingSenderId with yours
	messagingSenderId: "456393506172",
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
// [END initialize_firebase_in_sw]

// If you would like to customize notifications that are received in the
// background (Web app is closed or not in browser focus) then you should
// implement this optional method.
// [START background_handler]
messaging.setBackgroundMessageHandler(function (payload) {
	console.log(
		"[firebase-messaging-sw.js] Received background message ",
		payload
	);
	// Customize notification here
	payload = payload.data;
	const notificationTitle = payload.title;
	const notificationOptions = {
		body: payload.body,
		icon: payload.icon_url,
	};

	self.addEventListener("notificationclick", function (event) {
		event.notification.close();
		clients.openWindow(payload.url);
	});

	return self.registration.showNotification(
		notificationTitle,
		notificationOptions
	);
});
// [END background_handler]
