document.addEventListener('DOMContentLoaded', function() {
    const orderStatusElement = document.getElementById('order-status');
    const retryPaymentButton = document.getElementById('retry-payment-btn');
    const orderId = orderStatusElement?.dataset.orderId;

    if (!orderId || !orderStatusElement) return;

    // Statuses that should stop polling
    const finalStatuses = ['paid', 'delivered', 'cancelled', 'refunded'];
    
    // Update status display
    function updateStatusDisplay(data) {
        // Update status text and color
        orderStatusElement.textContent = data.status_display;
        orderStatusElement.className = `badge bg-${data.status_color}`;

        // Show/hide retry payment button
        if (retryPaymentButton) {
            if (['payment_failed', 'awaiting_payment', 'pending'].includes(data.status)) {
                retryPaymentButton.style.display = 'inline-block';
            } else {
                retryPaymentButton.style.display = 'none';
            }
        }

        // If there's a payment error, show it
        const errorElement = document.getElementById('payment-error');
        if (errorElement && data.last_error) {
            errorElement.textContent = data.last_error;
            errorElement.style.display = 'block';
        }

        // Update payment details if available
        const paymentDetailsElement = document.getElementById('payment-details');
        if (paymentDetailsElement && data.stripe_status) {
            let details = `
                <p><strong>Status plată:</strong> ${data.stripe_status}</p>
                <p><strong>Metodă plată:</strong> ${data.payment_method || 'N/A'}</p>
                <p><strong>Sumă:</strong> ${data.amount} Lei</p>
            `;
            if (data.last_attempt) {
                details += `<p><strong>Ultima încercare:</strong> ${new Date(data.last_attempt).toLocaleString('ro-RO')}</p>`;
            }
            paymentDetailsElement.innerHTML = details;
        }

        // Return true if we should stop polling
        return finalStatuses.includes(data.status);
    }

    // Poll for status updates
    function pollPaymentStatus() {
        fetch(`/order/${orderId}/payment-status/`)
            .then(response => response.json())
            .then(data => {
                const shouldStop = updateStatusDisplay(data);
                if (!shouldStop) {
                    // Continue polling every 5 seconds
                    setTimeout(pollPaymentStatus, 5000);
                }
            })
            .catch(error => {
                console.error('Error polling payment status:', error);
                // Retry after 10 seconds on error
                setTimeout(pollPaymentStatus, 10000);
            });
    }

    // Start polling
    pollPaymentStatus();

    // Handle retry payment button
    if (retryPaymentButton) {
        retryPaymentButton.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.href;
            
            // Show loading state
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Se procesează...';
            
            // Redirect to retry payment URL
            window.location.href = url;
        });
    }
});