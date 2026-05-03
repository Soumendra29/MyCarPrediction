const form = document.getElementById('signupForm');
const msg = document.getElementById('msg');

if (form) {
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const pass = document.getElementById('password').value;
    const confirm = document.getElementById('confirm').value;

    if (!name || !email || !pass || !confirm) {
      msg.style.display = 'block';
      msg.style.color = 'red';
      msg.innerText = 'Please fill in all fields.';
      return;
    }

    if (pass !== confirm) {
      msg.style.display = 'block';
      msg.style.color = 'red';
      msg.innerText = 'Passwords do not match ❌';
      return;
    }

    msg.style.display = 'block';
    msg.style.color = '#00ffae';
    msg.innerText = 'Account created successfully ✔';

    setTimeout(() => {
      window.location.href = 'login.html';
    }, 1500);
  });
}
