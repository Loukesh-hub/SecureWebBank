// script.js
// SecureWebBank - Frontend JavaScript

document.addEventListener("DOMContentLoaded", () => {
    console.log("SecureWebBank loaded successfully!");

    // Navigation
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            navLinks.forEach(item => item.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Deposit
    const depositBtn = document.getElementById("depositBtn");

    if (depositBtn) {
        depositBtn.addEventListener("click", () => {
            const amount = Number(document.getElementById("depositAmount")?.value);

            if (!Number.isFinite(amount) || amount <= 0) {
                alert("Please enter a valid deposit amount.");
                return;
            }

            alert("Deposit request submitted.");
        });
    }

    // Withdrawal
    const withdrawBtn = document.getElementById("withdrawBtn");

    if (withdrawBtn) {
        withdrawBtn.addEventListener("click", () => {
            const amount = Number(document.getElementById("withdrawAmount")?.value);

            if (!Number.isFinite(amount) || amount <= 0) {
                alert("Please enter a valid withdrawal amount.");
                return;
            }

            alert("Withdrawal request submitted.");
        });
    }

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            const confirmLogout = confirm("Are you sure you want to logout?");

            if (confirmLogout) {
                window.location.href = "login.html";
            }
        });
    }
});