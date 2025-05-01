document.getElementById('profile-form').addEventListener('submit', function(event) {
    const nameInput = document.getElementById('name');
    if (!nameInput.value)
     {
        event.preventDefault()
        alert('Name is required!')
    }
    
    
});

