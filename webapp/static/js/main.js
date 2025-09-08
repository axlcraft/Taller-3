// Agregar producto al carrito
function addToCart(productId) {
    fetch(`/add_to_cart/${productId}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

// Actualizar cantidad en el carrito
function updateCartQuantity(itemId, quantity) {
    fetch(`/update_cart/${itemId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    });
}

// Remover producto del carrito
function removeFromCart(itemId) {
    fetch(`/remove_from_cart/${itemId}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    });
}
