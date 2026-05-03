const form = document.getElementById("loginForm");

form.addEventListener("submit", function(e){
    e.preventDefault();

    const email = document.getElementById("email");
    const password = document.getElementById("password");

    // Click animation
    form.classList.add("clicked");
    setTimeout(()=> form.classList.remove("clicked"), 300);

    if(email.value.trim() === "" || password.value.trim() === ""){
        shake(form);
        return;
    }

    // Success animation
    successAnim();

    
    setTimeout(()=>{
        window.location.replace("http://127.0.0.1:8000/index.html");
    }, 1200);

    function shake(el){
        el.style.animation = "shake 0.4s";
        setTimeout(()=> el.style.animation = "", 400);
    }

    function successAnim(){
        document.querySelector(".login-box").style.boxShadow = "0 0 60px rgba(0,255,150,0.8)";
    }
});

/* Shake animation */
const style = document.createElement('style');
style.innerHTML = `
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  50% { transform: translateX(6px); }
  75% { transform: translateX(-6px); }
  100% { transform: translateX(0); }
}`;
document.head.appendChild(style);