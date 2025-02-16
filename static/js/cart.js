function updateQuantity(productId, newQuantity) {
    const data = {
        product_id: productId,
        quantity: newQuantity,
    };

    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    });
}

function removeFromCart(productId) {
    const data = {
        product_id: productId
    };

    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        window.location.reload();
    });
}

function decrementQuantity(productId, currentQuantity) {
    if (currentQuantity > 1) {
        updateQuantity(productId, currentQuantity - 1);
    }
}

function incrementQuantity(productId, currentQuantity, maxQuantity) {
    if (currentQuantity < maxQuantity) {
        updateQuantity(productId, currentQuantity + 1);
    }
}

// Initialize cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle quantity update forms
    document.querySelectorAll('form[action="/cart/update/"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const productId = form.querySelector('[name=product_id]').value;
            const quantity = parseInt(form.querySelector('button[type=submit][name=quantity]').value);
            updateQuantity(productId, quantity);
        });
    });

    // Handle remove from cart forms
    document.querySelectorAll('form[action="/cart/remove/"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const productId = form.querySelector('[name=product_id]').value;
            removeFromCart(productId);
        });
    });

    // Auto-hide alerts after 3 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 3000);
});
