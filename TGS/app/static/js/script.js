// Get elements
const btnLoginPopup = document.querySelector('.btnLogin-popup');
const wrapper = document.querySelector('.wrapper');
const iconClose = document.querySelector('.icon-close');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');  // Changed to '.login-link' to match correct class

// Show login form when Login button is clicked
btnLoginPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');  // Show the popup
    document.querySelector('.form-box.login').classList.add('active');  // Show the login form
    document.querySelector('.form-box.register').classList.remove('active');  // Hide the register form
});

// Close the form when close icon is clicked
iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');  // Hide the popup
    document.querySelector('.form-box.login').classList.remove('active');  // Reset the login form
    document.querySelector('.form-box.register').classList.remove('active');  // Reset the register form
});

// Show the register form when "Register Now" is clicked
registerLink.addEventListener('click', (e) => {
    e.preventDefault();  // Prevent the default link behavior
    wrapper.classList.add('active');  // Activate the wrapper
    wrapper.classList.remove('active-popup');  // Hide login form popup
    document.querySelector('.form-box.login').classList.remove('active');  // Hide the login form
    document.querySelector('.form-box.register').classList.add('active');  // Show the register form
});

// Show the login form from register form when "Login Now" is clicked
loginLink.addEventListener('click', (e) => {
    e.preventDefault();  // Prevent the default link behavior
    wrapper.classList.remove('active');  // Deactivate the register form
    wrapper.classList.add('active-popup');  // Activate the login form popup
    document.querySelector('.form-box.register').classList.remove('active');  // Hide the register form
    document.querySelector('.form-box.login').classList.add('active');  // Show the login form
});
