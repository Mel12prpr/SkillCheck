document.addEventListener('DOMContentLoaded', () => {
  // Burger menu logic
  const burger = document.getElementById('burger');
  const navLinks = document.getElementById('nav-links');

  if (burger && navLinks) {
    burger.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }

  // Form validation logic
  const form = document.getElementById('quizForm');
  const errorMessage = document.getElementById('formError');

  if (form) {
    form.addEventListener('submit', function (e) {
      const inputs = form.querySelectorAll('input, textarea, select');
      let valid = true;
      let firstInvalidField = null;
      let errorTexts = [];

      // Reset visual errors
      inputs.forEach((input) => input.classList.remove('input-error'));
      errorMessage.innerText = '';

      inputs.forEach((input) => {
        const value = input.value.trim();
        const name = input.getAttribute('name');

        if (input.hasAttribute('required') && !value) {
          valid = false;
          errorTexts.push(`"${formatFieldName(name)}" is required.`);
          input.classList.add('input-error');
          if (!firstInvalidField) firstInvalidField = input;
        }

        // num_questions should be a number
        if (name === 'num_questions' && value && isNaN(value)) {
          valid = false;
          errorTexts.push('"Number of Questions" must be a valid number.');
          input.classList.add('input-error');
          if (!firstInvalidField) firstInvalidField = input;
        }
      });

      if (!valid) {
        e.preventDefault();
        errorMessage.innerText = errorTexts.join(' ');
        if (firstInvalidField) firstInvalidField.focus();
      }
    });

    // Optional live restriction for num_questions field
    const numInput = form.querySelector('input[name="num_questions"]');
    if (numInput) {
      numInput.addEventListener('input', () => {
        numInput.value = numInput.value.replace(/[^0-9]/g, '');
      });
    }
  }

  function formatFieldName(name) {
    // turns snake_case to Title Case (e.g. num_questions -> Number of Questions)
    return name.replace(/_/g, ' ')
               .replace(/\w\S*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1));
  }
});

//registration form validation
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");

  const username = form.username;
  const firstName = form.first_name;
  const lastName = form.last_name;
  const email = form.email;
  const password1 = form.password1;
  const password2 = form.password2;

  const errors = {
    username: document.getElementById("usernameError"),
    firstName: document.getElementById("firstNameError"),
    lastName: document.getElementById("lastNameError"),
    email: document.getElementById("emailError"),
    password1: document.getElementById("password1Error"),
    password2: document.getElementById("password2Error"),
  };

  // Show/hide password
  document.getElementById("togglePassword1").addEventListener("change", function () {
    password1.type = this.checked ? "text" : "password";
  });

  document.getElementById("togglePassword2").addEventListener("change", function () {
    password2.type = this.checked ? "text" : "password";
  });

  form.addEventListener("submit", function (e) {
    let valid = true;

    // Clear previous errors
    Object.values(errors).forEach(err => err.textContent = "");

    // Username: required, min 3 chars
    if (username.value.trim().length < 3) {
      errors.username.textContent = "Username must be at least 3 characters.";
      valid = false;
    }

    // First name
    if (firstName.value.trim() === "") {
      errors.firstName.textContent = "First name is required.";
      valid = false;
    }

    // Last name
    if (lastName.value.trim() === "") {
      errors.lastName.textContent = "Last name is required.";
      valid = false;
    }

    // Email: basic regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
      errors.email.textContent = "Enter a valid email address.";
      valid = false;
    }

    // Password: required, min 6 chars
    if (password1.value.length < 6) {
      errors.password1.textContent = "Password must be at least 8 characters.";
      valid = false;
    }

    // Password match
    if (password1.value !== password2.value) {
      errors.password2.textContent = "Passwords do not match.";
      valid = false;
    }

    if (!valid) {
      e.preventDefault(); // Stop form submission
    }
  });
});


// login form validation
document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const usernameError = document.getElementById('usernameError');
  const passwordError = document.getElementById('passwordError');
  const togglePassword = document.getElementById('togglePassword');

  loginForm.addEventListener('submit', function (e) {
    let valid = true;
    usernameError.textContent = '';
    passwordError.textContent = '';

    if (!usernameInput.value.trim()) {
      usernameError.textContent = 'Username is required';
      valid = false;
    }

    if (!passwordInput.value.trim()) {
      passwordError.textContent = 'Password is required';
      valid = false;
    }

    if (!valid) e.preventDefault();
  });

  togglePassword.addEventListener('change', function () {
    passwordInput.type = this.checked ? 'text' : 'password';
  });
});

// cookies

document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("accept-cookies");

  if (!localStorage.getItem("cookieAccepted")) {
    banner.style.display = "block";
  }

  acceptBtn?.addEventListener("click", function () {
    localStorage.setItem("cookieAccepted", "true");
    banner.style.display = "none";
  });
});

// fetch active users api
document.addEventListener("DOMContentLoaded", () => {
  const userList = document.getElementById("user-list");
  if (!userList) return;

  async function fetchUsers() {
    try {
      const res = await fetch("https://randomuser.me/api/?results=10");
      const data = await res.json();
      const users = data.results;

      userList.innerHTML = "";

      users.forEach(user => {
        const div = document.createElement("div");
        div.className = "floating-user";

        div.innerHTML = `
          <div class="avatar-container">
            <img src="${user.picture.large}" alt="${user.name.first}" class="floating-avatar" />
            <span class="status-dot online"></span>
          </div>
          <p class="floating-name">${user.name.first} ${user.name.last}</p>
        `;

        userList.appendChild(div);
      });
    } catch (err) {
      console.error("Failed to load users:", err);
      userList.innerHTML = "Could not load users.";
    }
  }

  fetchUsers();
});
