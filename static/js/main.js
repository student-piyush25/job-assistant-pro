const verifyRes = await fetch("/payment_success", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        razorpay_order_id: paymentResponse.razorpay_order_id,
        razorpay_payment_id: paymentResponse.razorpay_payment_id,
        razorpay_signature: paymentResponse.razorpay_signature
    })
});