document.querySelectorAll(".checkout-button").forEach(button => {
    button.addEventListener("click", function (event) {
        const ticketId = event.target.dataset.ticketId;

        console.log(document.getElementById('stripe-publishable-key').textContent);

        fetch(`/create-checkout-session/?ticket_id=${ticketId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.id) {
                const stripe = Stripe(document.getElementById('stripe-publishable-key').textContent);
                stripe.redirectToCheckout({ sessionId: data.id });
            } else {
                console.error("Error:", data.error);
            }
        })
        .catch(function (error) {
            console.error("Error:", error);
        });
    });
});  
