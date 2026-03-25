// ================= GREETING FUNCTIONALITY =================
function getGreeting() {
 const hour = new Date().getHours();

 if (hour < 12) return "Good Morning";
 if (hour < 17) return "Good Afternoon";
 if (hour < 21) return "Good Evening";
 return "Good Night";
}

window.onload = function () {
 const greeting = getGreeting();
 document.getElementById("greeting-text").innerText = greeting + " ";
};

// ================= CHAT FUNCTIONALITY =================

const chatForm = document.getElementById('chat-form');
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
let typingIndicator = null;

// ================= NEW MESSAGE BUTTON =================
const newMsgBtn = document.createElement("button");
newMsgBtn.innerText = "New messages ↓";
newMsgBtn.style.position = "fixed";
newMsgBtn.style.bottom = "0px"; // base (will be updated dynamically)
newMsgBtn.style.left = "50%";
newMsgBtn.style.transform = "translateX(-50%)";
newMsgBtn.style.padding = "8px 14px";
newMsgBtn.style.borderRadius = "20px";
newMsgBtn.style.border = "none";
newMsgBtn.style.background = "#003366";
newMsgBtn.style.color = "#fff";
newMsgBtn.style.cursor = "pointer";
newMsgBtn.style.display = "none";
newMsgBtn.style.zIndex = "1000";

document.body.appendChild(newMsgBtn);

// ================= SCROLL =================
function isUserNearBottom() {
 return (
 chatContainer.scrollHeight - chatContainer.scrollTop - chatContainer.clientHeight
 ) < 120;
}

newMsgBtn.onclick = () => {
 chatContainer.scrollTo({
 top: chatContainer.scrollHeight,
 behavior: "smooth"
 });
 newMsgBtn.style.display = "none";
};

chatContainer.addEventListener("scroll", () => {
 if (isUserNearBottom()) {
 newMsgBtn.style.display = "none";
 }
});

// ================= APPEND MESSAGE =================
function appendMessage(sender, text) {

 const msgWrapper = document.createElement('div');
 msgWrapper.className = `message-wrapper ${sender}`;

 const avatar = document.createElement('div');
 avatar.className = 'avatar';

 if (sender === "user") {
 avatar.innerHTML = `<i class="fas fa-user"></i>`;
 } else {
 avatar.innerHTML = `<i class="fas fa-headset"></i>`;
 }

 const msgDiv = document.createElement('div');
 msgDiv.className = `message ${sender}-message`;

 msgDiv.setAttribute("role","alert");
 msgDiv.setAttribute("aria-live","polite");

 // USER HEADER
 if (sender === "user") {
 const header = document.createElement("div");
 header.className = "user-header";
 header.innerHTML = `User`;
 msgDiv.appendChild(header);
 }

 // BOT HEADER
 if (sender === "bot") {
 const header = document.createElement("div");
 header.className = "bot-header";
 header.innerHTML = `Ayushman Assistant <span class="verified">✔</span>`;
 msgDiv.appendChild(header);
 }

 const messageText = document.createElement('div');
 messageText.className = "message-text";
 messageText.innerHTML = text;

 const time = document.createElement("div");
 time.className = "time";
 time.innerHTML = new Date().toLocaleTimeString([], {
 hour: '2-digit',
 minute: '2-digit'
 });

 msgDiv.appendChild(messageText);
 msgDiv.appendChild(time);

 // COPY BUTTON (BOT ONLY)
 if(sender === "bot"){
 const copyBtn = document.createElement("button");
 copyBtn.className = "copy-btn";
 copyBtn.innerHTML = `<i class="fas fa-copy"></i>`;
 copyBtn.onclick = () => navigator.clipboard.writeText(text);
 msgDiv.appendChild(copyBtn);
 }

 msgWrapper.appendChild(avatar);
 msgWrapper.appendChild(msgDiv);

 chatContainer.appendChild(msgWrapper);

 // FORCE SCROLL FOR USER + SMART FOR BOT
 if (sender === "user" || isUserNearBottom()) {
 setTimeout(() => {
 chatContainer.scrollTo({
 top: chatContainer.scrollHeight,
 behavior: "smooth"
 });
 }, 50);
 } else {
 newMsgBtn.style.display = "block";
 updateNewMsgBtnPosition(); 
 }
}

// ================= TYPING =================
function showTypingIndicator() {
 if (typingIndicator) return;

 typingIndicator = document.createElement('div');
 typingIndicator.className = 'message-wrapper bot';

 typingIndicator.innerHTML = `
 <div class="avatar"><i class="fas fa-headset"></i></div>
 <div class="message bot-message typing">
 <span class="dot"></span>
 <span class="dot"></span>
 <span class="dot"></span>
 </div>
 `;

 chatContainer.appendChild(typingIndicator);

 // ALWAYS SCROLL
 chatContainer.scrollTo({
 top: chatContainer.scrollHeight,
 behavior: "smooth"
 });
}

function removeTypingIndicator() {
 if (typingIndicator && chatContainer.contains(typingIndicator)) {
 chatContainer.removeChild(typingIndicator);
 typingIndicator = null;
 }
}

// ================= FORM SUBMIT =================
// ================= FORM SUBMIT =================
chatForm.addEventListener('submit', async (e) => {
 e.preventDefault();

 const query = userInput.value.trim();
 if (!query) return;

 // Expand chat from initial state
 if (chatCard.classList.contains("initial-state")) {
 chatCard.classList.remove("initial-state");
 chatCard.classList.add("expanded");
 document.querySelector(".greeting-box").style.display = "none";
 document.querySelector(".initial-message").style.display = "none";
 document.querySelector(".main-container").style.alignItems = "stretch";
 }

 // Check near-me BEFORE sending to server
// Only trigger GPS if user says "near me" / "nearby" WITHOUT a specific place name
 // "hospital near me" → GPS ✅
 // "hospital near bangalore" → send to server ✅
 const q = query.toLowerCase().trim();
 const gpsOnlyPhrases = ["near me", "nearby me", "around me", "close to me", 
 "nearest hospital", "closest hospital"];
 const isGpsQuery = gpsOnlyPhrases.some(p => q.includes(p));

 // Emergency without location = GPS
 const isEmergency = (q === "emergency" || q === "help" || 
 q === "urgent" || q === "sos" ||
 q.match(/^emergency\s*(hospital)?$/));

 if (isGpsQuery || isEmergency) {
 userInput.value = '';
 appendMessage('user', query);
 chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
 // Pass original query so specialization is preserved
 handleNearMeResponse(query);
 return;
 }

 appendMessage('user', query);
 chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
 userInput.value = '';

 const sendBtn = document.getElementById("send-btn");
 const micBtn = document.getElementById("mic-btn");
 sendBtn.disabled = true;
 userInput.disabled = true;
 if (micBtn) micBtn.disabled = true;

 showTypingIndicator();

 try {
 const response = await fetch('/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({ message: query })
 });

 const data = await response.json();
 removeTypingIndicator();

 if (response.ok && data.status === 'success') {
 appendMessage('bot', data.reply);
 // Show contextual follow-up chips
 setTimeout(() => showContextualChips(data.reply), 300);
 }else {
 appendMessage('bot', data.reply || "Something went wrong.");
 }

 } catch (err) {
 removeTypingIndicator();
 appendMessage('bot', "Error: Unable to reach the server.");
 console.error(err);
 } finally {
 sendBtn.disabled = false;
 userInput.disabled = false;
 if (micBtn) micBtn.disabled = false;
 userInput.focus();
 }
});

// ================= INITIAL =================
const chatCard = document.querySelector(".chat-card");

window.addEventListener("DOMContentLoaded", () => {
 chatCard.classList.add("initial-state");
 chatContainer.scrollTop = 0;
});

// ================= DARK MODE TOGGLE =================
const themeBtn = document.getElementById("theme-toggle");
const themeIcon = themeBtn.querySelector("i");

themeBtn.addEventListener("click", () => {
 document.body.classList.toggle("dark-mode");

 // icon animation switch
 if (document.body.classList.contains("dark-mode")) {
 themeIcon.classList.remove("fa-moon");
 themeIcon.classList.add("fa-sun");
 } else {
 themeIcon.classList.remove("fa-sun");
 themeIcon.classList.add("fa-moon");
 }
});

// ================= HEADER SHADOW ON SCROLL =================
const header = document.querySelector(".header");

window.addEventListener("scroll", () => {
 if (window.scrollY > 10) {
 header.style.boxShadow = "0 2px 10px rgba(0,0,0,0.3)";
 } else {
 header.style.boxShadow = "none";
 }
});

// ================= FIX BUTTON POSITION =================
function updateNewMsgBtnPosition() {
 const inputSection = document.querySelector(".input-section");
 if (!inputSection) return;

 const rect = inputSection.getBoundingClientRect();
 const spaceFromBottom = window.innerHeight - rect.top;

 newMsgBtn.style.bottom = (spaceFromBottom + 10) + "px";
}

// run initially + on resize
window.addEventListener("resize", updateNewMsgBtnPosition);
window.addEventListener("load", updateNewMsgBtnPosition); 


//direction + distance 
// ================= DIRECTIONS & DISTANCE =================

function getDirections(btn) {
 const address = btn.getAttribute("data-address");

 // Find distance span — it's inside .hospital-actions, sibling after map-toggle-btn
 const actionsDiv = btn.closest(".hospital-actions");
 const distanceSpan = actionsDiv ? actionsDiv.querySelector(".distance-info") : null;

 // Immediately open Google Maps — don't wait for geolocation
 const fallbackUrl = `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(address)}&travelmode=driving`;

 if (!navigator.geolocation) {
 window.open(fallbackUrl, "_blank");
 return;
 }

 const originalText = btn.innerHTML;
 btn.disabled = true;
 btn.textContent = "📍 Locating...";

 // Set a hard 5 second timeout — if geolocation takes too long, open fallback
 const geoTimeout = setTimeout(() => {
 btn.disabled = false;
 btn.innerHTML = originalText;
 window.open(fallbackUrl, "_blank");
 }, 5000);

 navigator.geolocation.getCurrentPosition(
 (position) => {
 clearTimeout(geoTimeout);

 const userLat = position.coords.latitude;
 const userLng = position.coords.longitude;

 const mapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${userLat},${userLng}&destination=${encodeURIComponent(address)}&travelmode=driving`;
 window.open(mapsUrl, "_blank");

 // Show distance
 fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
 .then(res => res.json())
 .then(data => {
 if (data && data.length > 0) {
 const destLat = parseFloat(data[0].lat);
 const destLng = parseFloat(data[0].lon);
 const dist = haversineDistance(userLat, userLng, destLat, destLng);
 if (distanceSpan) {
 distanceSpan.style.display = "inline";
 distanceSpan.textContent = `~${dist.toFixed(1)} km away`;
 }
 }
 }).catch(() => {});

 btn.disabled = false;
 btn.innerHTML = originalText;
 },
 () => {
 clearTimeout(geoTimeout);
 btn.disabled = false;
 btn.innerHTML = originalText;
 window.open(fallbackUrl, "_blank");
 },
 { timeout: 4500, maximumAge: 60000 }
 );
}
// Haversine formula: calculates crow-fly distance in km
function haversineDistance(lat1, lon1, lat2, lon2) {
 const R = 6371; // Earth radius in km
 const dLat = (lat2 - lat1) * Math.PI / 180;
 const dLon = (lon2 - lon1) * Math.PI / 180;
 const a =
 Math.sin(dLat / 2) * Math.sin(dLat / 2) +
 Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
 Math.sin(dLon / 2) * Math.sin(dLon / 2);
 const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
 return R * c;
}

//mini map display in the chat
/// ================= MAP TOGGLE =================
function toggleMap(btn) {
 const li = btn.closest("li");
 const mapContainer = li.querySelector(".mini-map-container");
 const iframe = mapContainer.querySelector(".mini-map-frame");
 const distLabel = mapContainer.querySelector(".map-distance-label");
 const address = btn.getAttribute("data-address");

 // Close if already open
// Close if already open
 if (mapContainer.style.display === "block") {
 mapContainer.style.display = "none";
 btn.textContent = "🗺️ Show Map";
 // Reset so next open gets fresh route with current GPS
 iframe.src = "";
 iframe.removeAttribute("data-loaded");
 if (distLabel) distLabel.style.display = "none";
 return;
 }

 mapContainer.style.display = "block";
 btn.textContent = "🗺️ Hide Map";

 // Show loading state in distance label
 if (distLabel) {
 distLabel.textContent = "📡 Getting your location for route...";
 distLabel.style.display = "block";
 distLabel.style.background = "#fff8e1";
 distLabel.style.color = "#7a5f00";
 }

 // Load destination-only map immediately as fallback
 // Only load if not already loaded
 if (!iframe.getAttribute("data-loaded")) {
 iframe.src = `https://maps.google.com/maps?q=${encodeURIComponent(address)}&output=embed&z=14`;
 iframe.setAttribute("data-loaded", "destination");
 }

 setTimeout(() => {
 mapContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
 }, 150);

 if (!navigator.geolocation) {
 if (distLabel) {
 distLabel.textContent = "📍 Showing hospital location (enable GPS for distance)";
 distLabel.style.background = "#f0f4f8";
 distLabel.style.color = "#555";
 }
 return;
 }

 navigator.geolocation.getCurrentPosition(
 (pos) => {
 const userLat = pos.coords.latitude;
 const userLng = pos.coords.longitude;

 // Only upgrade if not already showing directions
 if (iframe.getAttribute("data-loaded") !== "directions") {
 iframe.src = `https://maps.google.com/maps?saddr=${userLat},${userLng}&daddr=${encodeURIComponent(address)}&output=embed&z=11`;
 iframe.setAttribute("data-loaded", "directions");
 }

 // Calculate distance
 fetch(`https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(address)}`)
 .then(r => r.json())
 .then(data => {
 if (data && data.length > 0) {
 const destLat = parseFloat(data[0].lat);
 const destLng = parseFloat(data[0].lon);
 const dist = haversineDistance(userLat, userLng, destLat, destLng);
 if (distLabel) {
 distLabel.textContent = `📏 ~${dist.toFixed(1)} km from your location (straight-line) • Route shown below`;
 distLabel.style.display = "block";
 distLabel.style.background = "#e8f4e8";
 distLabel.style.color = "#1a5f2a";
 }
 } else {
 if (distLabel) {
 distLabel.textContent = "🗺️ Route from your location shown below";
 distLabel.style.background = "#e8f4e8";
 distLabel.style.color = "#1a5f2a";
 }
 }
 })
 .catch(() => {
 if (distLabel) {
 distLabel.textContent = "🗺️ Route from your location shown below";
 distLabel.style.background = "#e8f4e8";
 distLabel.style.color = "#1a5f2a";
 }
 });
 },
 () => {
 // GPS denied — keep destination map, update label
 if (distLabel) {
 distLabel.textContent = "📍 Showing hospital location (location access denied)";
 distLabel.style.background = "#fff3cd";
 distLabel.style.color = "#856404";
 }
 },
 { timeout: 5000, maximumAge: 60000 }
 );
}
// ================= EMERGENCY NEARBY =================
function findNearbyHospitals() {
 const btn = document.getElementById("emergency-btn");
 const status = document.getElementById("emergency-status");

 if (!navigator.geolocation) {
 status.textContent = "⚠️ Geolocation not supported.";
 return;
 }

 btn.disabled = true;
 status.textContent = "📡 Getting your location...";

 navigator.geolocation.getCurrentPosition(
 (position) => {
 const lat = position.coords.latitude;
 const lng = position.coords.longitude;

 btn.disabled = false;
 status.textContent = "";

 // Expand chat if in initial state
 const chatCard = document.querySelector(".chat-card");
 if (chatCard.classList.contains("initial-state")) {
 chatCard.classList.remove("initial-state");
 chatCard.classList.add("expanded");
 document.querySelector(".greeting-box").style.display = "none";
 const initMsg = document.querySelector(".initial-message");
 if (initMsg) initMsg.style.display = "none";
 document.querySelector(".main-container").style.alignItems = "stretch";
 const bb = document.getElementById("benefits-bar");
 if (bb) bb.style.display = "none";
 }
 // Step 1: Show the live nearby map immediately
 injectNearbyMapCard(lat, lng);

 // Step 2: Reverse geocode ONCE, then query backend
 fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
 .then(r => r.json())
 .then(data => {
 const county = data.address?.county || "";
 const state_district = data.address?.state_district || "";
 const city = data.address?.city || data.address?.town || "";
 const district = (county || state_district || city)
 .replace(" District", "")
 .toLowerCase()
 .trim();

 const query = district
 ? `hospital in ${district}`
 : `hospital near me`;

 // Show detected location as user message
 if (district) {
 appendMessage('user', `📍 Searching hospitals in: ${district.charAt(0).toUpperCase() + district.slice(1)}`);
 }

 showTypingIndicator();

 // Query backend with detected district
 fetch('/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({ message: query })
 })
 .then(r => r.json())
 .then(result => {
 removeTypingIndicator();
 if (result.status === 'success') {
 appendMessage('bot', result.reply);
 } else {
 appendMessage('bot', "Sorry, no hospitals found for your location.");
 }
 })
 .catch(() => {
 removeTypingIndicator();
 appendMessage('bot', "Error connecting to server.");
 });
 })
 .catch(() => {
 // Geocoding failed — still show map, ask user to type
 appendMessage('bot', "📍 Map shown above. Could not detect district — please type it, e.g. 'hospital in Mysuru'.");
 });
 },
 (err) => {
 btn.disabled = false;
 status.textContent = "⚠️ Location denied. Please enable location access.";
 },
 { timeout: 10000, enableHighAccuracy: true }
 );
}

function injectNearbyMapCard(lat, lng) {
 const container = document.getElementById("chat-container");

 const wrapper = document.createElement("div");
 wrapper.className = "message-wrapper bot";

 // Google Maps nearby hospitals embed
 const mapsUrl = `https://maps.google.com/maps?q=hospital+near+me&ll=${lat},${lng}&z=13&output=embed`;
 const directionsUrl = `https://www.google.com/maps/search/hospital+near+me/@${lat},${lng},13z`;

 wrapper.innerHTML = `
 <div class="avatar"><i class="fas fa-headset"></i></div>
 <div class="message bot-message">
 <div class="bot-header">Ayushman Assistant <span class="verified">✔</span></div>
 <div class="message-text">
 <p>🚨 <b>Nearest hospitals to your current location:</b></p>
 <div class="emergency-map-card">
 <iframe 
 src="${mapsUrl}"
 class="emergency-map-frame"
 allowfullscreen
 loading="lazy">
 </iframe>
 <a href="${directionsUrl}" target="_blank" class="open-maps-link">
 🗺️ Open Full Map in Google Maps
 </a>
 </div>
 </div>
 <div class="time">${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</div>
 </div>
 `;

 container.appendChild(wrapper);
 chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
}


// ================= NEAR ME HANDLER (triggered from chat form) =================
async function handleNearMeResponse(originalQuery = "") {
 if (!navigator.geolocation) {
 appendMessage('bot', "⚠️ Location not supported. Please type your district, e.g. 'hospital in Bengaluru'.");
 return;
 }

 appendMessage('bot', "📡 Detecting your location...");

 navigator.geolocation.getCurrentPosition(
 async (pos) => {
 const lat = pos.coords.latitude;
 const lng = pos.coords.longitude;

 // Show nearby map immediately
 injectNearbyMapCard(lat, lng);

 try {
 const geoRes = await fetch(
 `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`
 );
 const geoData = await geoRes.json();

 const county = geoData.address?.county || "";
 const state_district = geoData.address?.state_district || "";
 const city = geoData.address?.city || geoData.address?.town || "";
 const district = (county || state_district || city)
 .replace(" District", "")
 .toLowerCase()
 .trim();

 if (!district) {
 appendMessage('bot', "⚠️ Could not detect your district. Please type it, e.g. 'hospital in Mysuru'.");
 return;
 }

 appendMessage('bot', `📍 Detected: <b>${district.charAt(0).toUpperCase() + district.slice(1)}</b>. Finding PM-JAY hospitals...`);
 showTypingIndicator();

 // Preserve specialization from original query
 // e.g. "eye hospital near me" → "eye hospital in devanahalli"
 let finalQuery = `hospital in ${district}`;
 if (originalQuery) {
 const cleaned = originalQuery.toLowerCase()
 .replace(/near me|nearby me|around me|close to me|nearest|closest/gi, "")
 .trim();
 if (cleaned && cleaned !== "hospital" && cleaned !== "") {
 finalQuery = `${cleaned} in ${district}`;
 }
 }

 const chatRes = await fetch('/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({ message: finalQuery })
 });

 const chatData = await chatRes.json();
 removeTypingIndicator();

 if (chatData.status === 'success') {
 appendMessage('bot', chatData.reply);
 } else {
 appendMessage('bot', chatData.reply || "No hospitals found for your area.");
 }

 } catch (err) {
 removeTypingIndicator();
 console.error("Near me error:", err);
 appendMessage('bot', "⚠️ Could not fetch hospitals. Please try typing your district manually.");
 }
 },
 (err) => {
 console.error("Geolocation error:", err);
 
 const retryHtml = `
 ⚠️ <b>Location access was denied.</b><br><br>
 To find hospitals near you automatically:<br>
 <ol style="margin:6px 0; padding-left:18px;">
 <li>Click the 🔒 lock icon in your browser address bar</li>
 <li>Set <b>Location</b> to <b>Allow</b></li>
 <li>Refresh and try again</li>
 </ol>
 <button onclick="retryLocationRequest('${(originalQuery||'').replace(/'/g,"\\'")}') " 
 style="margin-top:8px; padding:7px 16px; background:#003366; color:white; 
 border:none; border-radius:20px; cursor:pointer; font-weight:600;">
 🔄 Try Again
 </button>
 <br><br>
 Or type your district manually, e.g. <b>'eye hospital in Mysuru'</b>
 `;
 appendMessage('bot', retryHtml);
 },
 { timeout: 8000, maximumAge: 60000 }
 );
}

// ================= RETRY LOCATION =================
function retryLocationRequest(originalQuery) {
 appendMessage('bot', "📡 Requesting location again...");

 navigator.geolocation.getCurrentPosition(
 async (pos) => {
 const lat = pos.coords.latitude;
 const lng = pos.coords.longitude;

 injectNearbyMapCard(lat, lng);

 try {
 const geoRes = await fetch(
 `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`
 );
 const geoData = await geoRes.json();

 const county = geoData.address?.county || "";
 const state_district = geoData.address?.state_district || "";
 const city = geoData.address?.city || geoData.address?.town || "";
 const district = (county || state_district || city)
 .replace(" District", "").toLowerCase().trim();

 if (!district) {
 appendMessage('bot', "⚠️ Still could not detect district. Please type it manually.");
 return;
 }

 appendMessage('bot', `📍 Detected: <b>${district.charAt(0).toUpperCase() + district.slice(1)}</b>. Finding hospitals...`);
 showTypingIndicator();

 let finalQuery = `hospital in ${district}`;
 if (originalQuery) {
 const cleaned = originalQuery.toLowerCase()
 .replace(/near me|nearby me|around me|closest|nearest/gi, "").trim();
 if (cleaned && cleaned !== "hospital") {
 finalQuery = `${cleaned} in ${district}`;
 }
 }

 const chatRes = await fetch('/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({ message: finalQuery })
 });
 const chatData = await chatRes.json();
 removeTypingIndicator();

 if (chatData.status === 'success') {
 appendMessage('bot', chatData.reply);
 } else {
 appendMessage('bot', "No hospitals found for your area.");
 }
 } catch (err) {
 removeTypingIndicator();
 appendMessage('bot', "⚠️ Error fetching hospitals. Please type your district manually.");
 }
 },
 () => {
 appendMessage('bot', `
 ❌ Location still denied.<br>
 Please go to browser settings → Site Settings → Location → Allow for this site.<br><br>
 Or type directly: <b>'eye hospital in Bengaluru'</b>
 `);
 },
 { timeout: 8000, maximumAge: 0 } // maximumAge: 0 forces fresh request
 );
}


// ================= SUGGESTION CHIPS =================
function fillQuery(text) {
 // Expand from initial state first
 if (chatCard.classList.contains("initial-state")) {
 chatCard.classList.remove("initial-state");
 chatCard.classList.add("expanded");
 const greetBox = document.querySelector(".greeting-box");
 if (greetBox) greetBox.style.display = "none";
 const initMsg = document.querySelector(".initial-message");
 if (initMsg) initMsg.style.display = "none";
 document.querySelector(".main-container").style.alignItems = "stretch";
 // Hide benefits bar when chat starts
 const bb = document.getElementById("benefits-bar");
 if (bb) bb.style.display = "none";
 }
 userInput.value = text;
 userInput.focus();
 // Small delay so DOM updates first
 setTimeout(() => {
 chatForm.dispatchEvent(new Event('submit'));
 }, 50);
}

// Contextual follow-up chips shown after bot responds
const CONTEXTUAL_CHIPS = {
 eye: ["👁️ Eye hospital near me", "Glaucoma specialist", "Cataract surgery hospital"],
 heart: ["❤️ Cardiology near me", "Heart surgery hospital", "ECG test hospital"],
 dental: ["🦷 Dental implants", "Root canal hospital", "Oral surgery"],
 bone: ["🦴 Fracture treatment", "Joint replacement", "Spine specialist"],
 child: ["👶 NICU hospital", "Child vaccination", "Paediatric surgery"],
 emergency: ["🚨 24hr emergency", "Trauma centre", "ICU hospital"],
 general: ["🏥 Hospital near me", "Government hospital", "Multi-specialty hospital"],
};

function showContextualChips(botReply) {
 const text = botReply.toLowerCase();
 let chips = CONTEXTUAL_CHIPS.general;

 if (text.includes("eye") || text.includes("ophthalm")) chips = CONTEXTUAL_CHIPS.eye;
 else if (text.includes("heart") || text.includes("cardi")) chips = CONTEXTUAL_CHIPS.heart;
 else if (text.includes("dental") || text.includes("tooth")) chips = CONTEXTUAL_CHIPS.dental;
 else if (text.includes("ortho") || text.includes("bone")) chips = CONTEXTUAL_CHIPS.bone;
 else if (text.includes("paed") || text.includes("child")) chips = CONTEXTUAL_CHIPS.child;
 else if (text.includes("emergency")) chips = CONTEXTUAL_CHIPS.emergency;

 const chipBar = document.createElement("div");
 chipBar.className = "floating-chips";
 chips.forEach(label => {
 const btn = document.createElement("button");
 btn.className = "floating-chip";
 btn.textContent = label;
 btn.onclick = () => {
 chipBar.remove();
 fillQuery(label.replace(/^[^\w₹]*/, "").trim());
 };
 chipBar.appendChild(btn);
 });

 // Append below last bot message
 const lastBot = [...document.querySelectorAll(".message-wrapper.bot")].pop();
 if (lastBot) lastBot.after(chipBar);

 chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
}
/*```

---

## Final structure of `1.js` REFERENCE:
```
getGreeting()
window.onload
chatForm, chatContainer, userInput declarations
newMsgBtn setup
isUserNearBottom()
newMsgBtn.onclick
chatContainer scroll listener
appendMessage()
showTypingIndicator()
removeTypingIndicator()
chatForm submit listener 
chatCard / DOMContentLoaded
dark mode toggle
header shadow scroll
updateNewMsgBtnPosition()
getDirections()
haversineDistance()
toggleMap()
findNearbyHospitals() 
injectNearbyMapCard()
handleNearMeResponse() */