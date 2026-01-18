const API = "http://127.0.0.1:5000";

let user = JSON.parse(localStorage.getItem("userProfile"));
let onboarded = localStorage.getItem("onboardingCompleted") === "true";

// Premium Features - Streak & Stats
let stats = JSON.parse(localStorage.getItem("userStats")) || {
  streak: 0,
  totalWorkouts: 0,
  totalCalories: 0,
  joinDate: new Date().toISOString(),
  achievements: []
};

window.onload = () => {
  if (!onboarded || !user) {
    document.getElementById("onboarding").style.display = "block";
    document.getElementById("dashboard").style.display = "none";
    document.querySelector("nav").style.display = "none";
  } else {
    document.getElementById("onboarding").style.display = "none";
    document.getElementById("dashboard").style.display = "block";
    document.querySelector("nav").style.display = "flex";
    updateStreak();
    tab("home");
  }
};

function tab(id) {
  document.querySelectorAll(".tab").forEach(t => t.style.display = "none");
  document.getElementById(id).style.display = "block";
  if (id === "home") loadHome();
  if (id === "diet") loadDiet();
  if (id === "profile") loadProfile();
  if (id === "workout") loadWorkout();
  if (id === "supplements") loadSupplements();
  if (id === "tips") loadTips();
}

/* ---------- ONBOARDING ---------- */
function completeOnboarding() {
  const name = obName.value.trim();
  const age = Number(obAge.value);
  const weight = Number(obWeight.value);
  const height = Number(obHeight.value);
  const gender = obGender.value;
  const goal = obGoal.value;

  if (!name || !age || !weight || !height || !gender || !goal) {
    alert("Fill all details");
    return;
  }

  user = { name, age, weight, height, gender, goal };
  localStorage.setItem("userProfile", JSON.stringify(user));
  localStorage.setItem("onboardingCompleted", "true");

  document.getElementById("onboarding").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
  document.querySelector("nav").style.display = "flex";
  tab("home");
}


/* ---------- SAVE PROFILE ---------- */
function loadProfile() {
  if (!user) return;

  // Header
  document.getElementById("profileName").innerText = user.name;
  document.getElementById("profileGoal").innerText = user.goal;

  // Stats
  document.getElementById("profileAge").innerText = user.age;
  document.getElementById("profileWeight").innerText = user.weight + " kg";
  document.getElementById("profileHeight").innerText = user.height + " cm";

  const bmi = (user.weight / ((user.height / 100) ** 2)).toFixed(1);
  document.getElementById("profileBMI").innerText = bmi;

  // Form values
  nameInput.value = user.name;
  ageInput.value = user.age;
  weightInput.value = user.weight;
  heightInput.value = user.height;
  goalInput.value = user.goal;
}
/* ================= PROFILE PHOTO UPLOAD ================= */

const photoInput = document.getElementById("photoInput");
const profilePhoto = document.getElementById("profilePhoto");
const avatarIcon = document.getElementById("avatarIcon");

if (photoInput) {
  photoInput.onchange = () => {
    const file = photoInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      profilePhoto.src = reader.result;
      profilePhoto.hidden = false;
      avatarIcon.style.display = "none";
      localStorage.setItem("profilePhoto", reader.result);
    };
    reader.readAsDataURL(file);
  };

  // Load saved photo on refresh
  const savedPhoto = localStorage.getItem("profilePhoto");
  if (savedPhoto) {
    profilePhoto.src = savedPhoto;
    profilePhoto.hidden = false;
    avatarIcon.style.display = "none";
  }
}
function drawChart() {
  const ctx = weeklyChart.getContext("2d");
  ctx.clearRect(0,0,300,150);

  const data = [1800, 2000, 1900, 2100, 2200, 2000, 2300];
  ctx.fillStyle = "#4f46e5";

  data.forEach((v,i)=>{
    ctx.fillRect(i*40,150-v/20,30,v/20);
  });
}
drawChart();

/* ----------HOME TAB ---------- */
async function loadHome() {
  const res = await fetch(`${API}/home`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });

  const data = await res.json();

  // Show Streak Badge
  const streakBadge = document.querySelector(".section-title");
  if (streakBadge) {
    streakBadge.innerHTML = `🏠 Daily Overview - ${getStreakBadge()} (${stats.streak} day${stats.streak !== 1 ? 's' : ''})`;
  }

  // TEXT VALUES
  document.getElementById("calText").innerText = data.calories;
  document.getElementById("proText").innerText = data.protein;
  document.getElementById("waterText").innerText = data.water;

  // RING SHADOWS & EFFECTS (Gradients are in CSS)
  document.getElementById("calRing").style.boxShadow = "0 12px 30px rgba(99, 102, 241, 0.3)";
  document.getElementById("proRing").style.boxShadow = "0 12px 30px rgba(16, 185, 129, 0.3)";
  document.getElementById("waterRing").style.boxShadow = "0 12px 30px rgba(6, 182, 212, 0.3)";

  // WEEKLY WORKOUT
  const list = document.getElementById("weeklyWorkout");
  list.innerHTML = "";
  data.weekly_workout.forEach(d => {
    list.innerHTML += `<li>${d.day}: ${d.focus}</li>`;
  });
}
/* ---------- DIET ---------- */
async function loadDiet() {
  const res = await fetch(`${API}/diet`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });

  const data = await res.json();

  // ===== UPDATE SUMMARY CARDS =====
  document.getElementById("dietCalories").innerText =
    `${data.target_calories} kcal`;

  document.getElementById("dietProtein").innerText =
    `${data.target_protein} g`;

  // ===== MEAL CARDS =====
  let html = "";

  ["breakfast", "lunch", "dinner"].forEach(meal => {
    html += `<div class="meal-card">
      <h3>${meal.toUpperCase()}</h3>`;

    data[meal].forEach(item => {
      html += `
        <div class="food-row">
          <span>${item.food}</span>
          <span>${item.calories} kcal | ${item.protein} g</span>
        </div>`;
    });

    html += `</div>`;
  });

  document.getElementById("dietMeals").innerHTML = html;
}

function saveProfile() {
  localStorage.setItem("userProfile", JSON.stringify(user));
  tab("diet");   // 🔥 important
}

function resetProfile() {
  if (confirm("Are you sure you want to reset your profile?")) {
    localStorage.removeItem("userProfile");
    localStorage.removeItem("onboardingCompleted");
    localStorage.removeItem("profilePhoto");
    localStorage.removeItem("userStats");
    location.reload();
  }
}

// ===== PREMIUM FEATURES =====
function updateStreak() {
  const today = new Date().toDateString();
  const lastActive = localStorage.getItem("lastActive");
  
  if (lastActive !== today) {
    stats.streak += 1;
    stats.totalWorkouts += 1;
    localStorage.setItem("lastActive", today);
    localStorage.setItem("userStats", JSON.stringify(stats));
    
    if (stats.streak % 7 === 0) {
      showAchievement(`🏆 ${stats.streak} Day Streak!`);
    }
  }
}

function showAchievement(message) {
  const div = document.createElement("div");
  div.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    font-weight: 600;
    z-index: 9999;
    animation: slideInRight 0.5s ease;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
  `;
  div.innerText = message;
  document.body.appendChild(div);
  
  setTimeout(() => div.remove(), 3000);
}

function getStreakBadge() {
  if (stats.streak >= 30) return "🔥 Legend";
  if (stats.streak >= 7) return "⭐ Star";
  if (stats.streak >= 3) return "🌟 Rising";
  return "🆕 Beginner";
}
/* ---------- FOOD SCAN ---------- */
async function scanFood() {
  const food = document.getElementById("scanFoodInput").value.trim();
  const resultDiv = document.getElementById("scanResult");

  if (!food) {
    alert("Please enter a food name");
    return;
  }

  resultDiv.innerHTML = "Scanning...";

  try {
   const res = await fetch(`${API}/scan-food`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ food }),
    });

    const data = await res.json();

    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
      return;
    }

    resultDiv.innerHTML = `
      <div class="card">
        <h3>🍽 ${data.food}</h3>
        <p>🔥 Calories: <b>${data.calories}</b> kcal</p>
        <p>💪 Protein: <b>${data.protein}</b> g</p>
        <p>📂 Category: ${data.category || "N/A"}</p>
      </div>
    `;
  } catch (err) {
    resultDiv.innerHTML = `<p style="color:red">Scan failed</p>`;
  }
}

/* ---------- WORKOUT ---------- */
async function loadWorkout() {
  const res = await fetch(`${API}/workout`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal: user.goal })
  });

  const data = await res.json();
  const grid = document.getElementById("workoutGrid");
  grid.innerHTML = "";

  data.forEach(day => {
    let exercisesHTML = "";

    day.exercises.forEach(ex => {
      exercisesHTML += `
        <div class="exercise">
          <span class="equipment">${ex.equipment}</span>
          <h4>${ex.name}</h4>
          <small>Sets: ${ex.sets} | Reps: ${ex.reps} | Rest: ${ex.rest}</small>
          <small>Variations: ${ex.variations?.join(", ") || "-"}</small>
        </div>
      `;
    });

    grid.innerHTML += `
      <div class="workout-day">
        <div class="workout-header">
          <h3>${day.day}</h3>
          <span class="focus-badge">${day.focus}</span>
        </div>
        ${exercisesHTML}
      </div>
    `;
  });
}

/* ---------- SUPPLEMENTS ---------- */
async function loadSupplements() {
  const res = await fetch(`${API}/supplements`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal: user.goal })
  });

  const data = await res.json();
  const grid = document.getElementById("supplementsGrid");
  grid.innerHTML = "";

  data.forEach(s => {
    grid.innerHTML += `
      <div class="supplement-card">
        <span class="supplement-tag">${user.goal}</span>
        <h3>${s.name}</h3>
        <p><strong>Why:</strong> ${s.reason}</p>
        <p><strong>Dosage:</strong> ${s.dosage}</p>
        <p><strong>Timing:</strong> ${s.timing}</p>
        <p><strong>Warning:</strong> ${s.warning}</p>
        <a href="${s.link}" target="_blank" class="buy-btn">
          Buy on HyugaLife →
        </a>
      </div>
    `;
  });
}
/* ===== PREMIUM TIPS DATA ===== */
const TIPS = [
  {
    title: "🔥 Fat Loss Tip",
    description:
      "Focus on protein-rich meals and maintain a calorie deficit. Walk at least 7–10k steps daily.",
    tag: "Weight Loss",
  },
  {
    title: "💪 Muscle Gain Tip",
    description:
      "Progressive overload + enough protein (1.6–2.2g/kg bodyweight) is key to muscle growth.",
    tag: "Muscle Gain",
  },
  {
    title: "🥗 Diet Tip",
    description:
      "Include complex carbs like oats, rice, and fruits instead of refined sugar.",
    tag: "Nutrition",
  },
  {
    title: "🧠 Recovery Tip",
    description:
      "Sleep 7–9 hours daily. Muscle grows during recovery, not during workouts.",
    tag: "Recovery",
  },
  {
    title: "🏃 Cardio Tip",
    description:
      "Low-intensity cardio (walking, cycling) burns fat without muscle loss.",
    tag: "Cardio",
  },
  {
    title: "💧 Hydration Tip",
    description:
      "Drink at least 3–4 liters of water daily for optimal performance.",
    tag: "Hydration",
  },
];

/* ===== LOAD TIPS ===== */
function loadTips() {
  const container = document.getElementById("tipsContainer");
  if (!container) return;

  container.innerHTML = "";

  TIPS.forEach((tip, index) => {
    const card = document.createElement("div");
    card.className = "tip-card";
    card.style.animationDelay = `${index * 0.08}s`;

    card.innerHTML = `
      <h3>${tip.title}</h3>
      <p>${tip.description}</p>
      <span class="tip-tag">${tip.tag}</span>
    `;

    container.appendChild(card);
  });
}
/* ---------- AI CHAT ---------- */
function addMessage(text, type) {
  const chat = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.className = `msg ${type}`;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendAI() {
  const input = document.getElementById("aiInput");
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";

  const res = await fetch(`${API}/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, user })
  });

  const data = await res.json();
  addMessage(data.reply, "ai");
}

function quickAsk(type) {
  const map = {
    calories: "How many calories should I eat?",
    protein: "How much protein do I need?",
    workout: "Best workout for my goal",
    motivation: "Give me motivation"
  };
  document.getElementById("aiInput").value = map[type];
  sendAI();
}
document.addEventListener("DOMContentLoaded", () => {
  const photoInput = document.getElementById("photoInput");
  const profilePhoto = document.getElementById("profilePhoto");
  const avatarIcon = document.getElementById("avatarIcon");

  if (!photoInput || !profilePhoto || !avatarIcon) {
    console.error("Avatar elements not found");
    return;
  }

  photoInput.addEventListener("change", () => {
    const file = photoInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      profilePhoto.src = reader.result;
      profilePhoto.style.display = "block";
      avatarIcon.style.display = "none";
      localStorage.setItem("profilePhoto", reader.result);
    };
    reader.readAsDataURL(file);
  });

  // Load saved photo
  const savedPhoto = localStorage.getItem("profilePhoto");
  if (savedPhoto) {
    profilePhoto.src = savedPhoto;
    profilePhoto.style.display = "block";
    avatarIcon.style.display = "none";
  }
});
