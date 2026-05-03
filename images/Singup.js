const form = document.getElementById('signupForm');
const msg = document.getElementById('msg');

form.addEventListener('submit', function(e){
  e.preventDefault();

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const pass = document.getElementById('password').value;
  const confirm = document.getElementById('confirm').value;

  if(pass !== confirm){
    msg.style.display = 'block';
    msg.style.color = 'red';
    msg.innerText = 'Passwords do not match ❌';
    return;
  }

  msg.style.display = 'block';
  msg.style.color = '#00ffae';
  msg.innerText = 'Account created successfully ✔';

  // fake signup success redirect
  setTimeout(()=>{
    window.location.href = 'login.html';
  },1500);
});