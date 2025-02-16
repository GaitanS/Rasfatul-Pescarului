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

// Auto-hide alerts after 3 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 3000);
});