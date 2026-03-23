/**
 * Authentication page logic (login & register).
 */

// --- Password visibility toggle ---
const toggleBtn = document.getElementById("toggle-password");
if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        const input = document.getElementById("password");
        const isHidden = input.type === "password";
        input.type = isHidden ? "text" : "password";
        toggleBtn.innerHTML = isHidden
            ? `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
               </svg>`
            : `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
               </svg>`;
    });
}

// --- Helper: show error ---
function showError(msg) {
    const el = document.getElementById("error-msg");
    el.textContent = msg;
    el.classList.remove("hidden");
}

function hideError() {
    document.getElementById("error-msg").classList.add("hidden");
}

// --- Helper: show success ---
function showSuccess(msg) {
    const el = document.getElementById("success-msg");
    if (el) {
        el.textContent = msg;
        el.classList.remove("hidden");
    }
}

// --- Password strength meter (register page) ---
const passwordInput = document.getElementById("password");
const strengthContainer = document.getElementById("password-strength");

if (passwordInput && strengthContainer) {
    passwordInput.addEventListener("input", () => {
        const val = passwordInput.value;
        if (!val) {
            strengthContainer.classList.add("hidden");
            return;
        }
        strengthContainer.classList.remove("hidden");

        let score = 0;
        if (val.length >= 8) score++;
        if (/[a-z]/.test(val) && /[A-Z]/.test(val)) score++;
        if (/\d/.test(val)) score++;
        if (/[^a-zA-Z0-9]/.test(val)) score++;

        const colors = ["bg-red-500", "bg-orange-500", "bg-yellow-500", "bg-green-500"];
        const labels = ["Weak", "Fair", "Good", "Strong"];

        for (let i = 1; i <= 4; i++) {
            const bar = document.getElementById(`str-${i}`);
            bar.className = `h-1 flex-1 rounded-full ${i <= score ? colors[score - 1] : "bg-gray-700"}`;
        }
        document.getElementById("strength-text").textContent = labels[score - 1] || "";
    });
}

// --- Password match check (register page) ---
const confirmInput = document.getElementById("confirm-password");
if (confirmInput && passwordInput) {
    confirmInput.addEventListener("input", () => {
        const matchEl = document.getElementById("password-match");
        if (!confirmInput.value) {
            matchEl.classList.add("hidden");
            return;
        }
        matchEl.classList.remove("hidden");
        if (passwordInput.value === confirmInput.value) {
            matchEl.textContent = "Passwords match";
            matchEl.className = "text-xs mt-1 text-green-400";
        } else {
            matchEl.textContent = "Passwords do not match";
            matchEl.className = "text-xs mt-1 text-red-400";
        }
    });
}

// --- Login form ---
const loginForm = document.getElementById("login-form");
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const spinner = document.getElementById("login-spinner");
        const btn = document.getElementById("login-btn");

        btn.disabled = true;
        spinner.classList.remove("hidden");

        try {
            const res = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                showError(data.detail || "Invalid email or password");
                return;
            }

            // Store token and redirect
            localStorage.setItem("access_token", data.access_token);
            window.location.href = "/";
        } catch (err) {
            showError("Unable to connect to server. Please try again.");
        } finally {
            btn.disabled = false;
            spinner.classList.add("hidden");
        }
    });
}

// --- Register form ---
const registerForm = document.getElementById("register-form");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError();

        const fullName = document.getElementById("full-name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;
        const spinner = document.getElementById("register-spinner");
        const btn = document.getElementById("register-btn");

        // Client-side validation
        if (password.length < 8) {
            showError("Password must be at least 8 characters");
            return;
        }
        if (password !== confirmPassword) {
            showError("Passwords do not match");
            return;
        }

        btn.disabled = true;
        spinner.classList.remove("hidden");

        try {
            const res = await fetch("/api/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name: fullName, email, password }),
            });

            const data = await res.json();

            if (!res.ok) {
                showError(data.detail || "Registration failed");
                return;
            }

            showSuccess("Account created! Redirecting to login...");
            setTimeout(() => {
                window.location.href = "/login";
            }, 1500);
        } catch (err) {
            showError("Unable to connect to server. Please try again.");
        } finally {
            btn.disabled = false;
            spinner.classList.add("hidden");
        }
    });
}
