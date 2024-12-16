document.querySelectorAll(".checkout-button").forEach(button => {
    button.addEventListener("click", function (event) {
        const ticketId = event.target.dataset.ticketId;

        console.log("Button clicked for ticket ID: ", ticketId);

        console.log("Stripe Publishable Key:", document.getElementById('stripe-publishable-key').textContent);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/create-checkout-session/?ticket_id=${ticketId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, 
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {

            console.log("Session Data:", data);

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
