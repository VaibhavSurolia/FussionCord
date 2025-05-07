document.getElementById("signupForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the default form submission
  
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const phone = document.getElementById("phone").value;
  
    try {
      const response = await fetch("https://fussioncord.onrender.com/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
      });
  
      const result = await response.json();
      if (response.ok) {
        document.getElementById("message").innerText = "Signup successful!";
      } else {
        document.getElementById("message").innerText = "Error: " + result.message;
      }
    } catch (error) {
      document.getElementById("message").innerText = "Network error: " + error.message;
    }
  });
  