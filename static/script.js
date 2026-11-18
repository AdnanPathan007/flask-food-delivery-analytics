// ======================================================
// SESSION CUSTOMER (created once per visit to index)
// ======================================================

function createCustomer() {
    return {
        customer_id: "CUST_" + Date.now(),
        name: "User_" + Math.floor(Math.random() * 1000),
        city: ["Aurangabad","Pune","Mumbai","Nagpur"][Math.floor(Math.random()*4)]
    };
}

// create new only when entering home page
if (window.location.pathname === "/") {
    sessionStorage.clear();
    sessionStorage.setItem("customer", JSON.stringify(createCustomer()));
}

const customer = JSON.parse(sessionStorage.getItem("customer") || "{}");


// ======================================================
// GLOBAL CART + ORDER
// ======================================================

let cart = JSON.parse(sessionStorage.getItem("cart") || "[]");

let orderId = sessionStorage.getItem("order_id");
if (!orderId) {
    orderId = "ORD_" + Date.now();
    sessionStorage.setItem("order_id", orderId);
}


// ======================================================
// CONSISTENT EVENT FORMAT BUILDER
// ======================================================

function buildPayload(type, options = {}) {

    return {
        event_type: type,
        page: window.location.pathname,

        customer: customer,

        product: {
            name: options.product_name || "",
            price: options.product_price || 0
        },

        order: {
            order_id: orderId,
            total: options.total || 0
        },

        metadata: {
            link: options.link || "",
            element: options.element || ""
        },

        // common browser info
        user_agent: navigator.userAgent,
        screen_resolution: screen.width + "x" + screen.height,
        language: navigator.language,
        referrer: document.referrer,
        timestamp: new Date().toISOString(),
        device_type: /Mobi|Android/i.test(navigator.userAgent) ? "Mobile" : "Desktop"
    };
}


// ======================================================
// TRACK EVENT (single sender)
// ======================================================

function trackEvent(type, options = {}) {

    const payload = buildPayload(type, options);

    fetch("/log_click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    console.log("Tracked:", payload);
}


// ======================================================
// CLICK TRACKING
// ======================================================

document.addEventListener("click", e => {
    const el = e.target.closest(".track-click");
    if (!el) return;

    trackEvent("click", {
        link: el.innerText,
        element: el.tagName
    });
});


// ======================================================
// CART FUNCTIONS
// ======================================================

function addToCart(name, price) {

    cart.push({ name, price });
    sessionStorage.setItem("cart", JSON.stringify(cart));

    trackEvent("add_to_cart", {
        product_name: name,
        product_price: price
    });

    alert(name + " added to cart");
}


function renderCart() {

    const list = document.getElementById("cartItems");
    if (!list) return;

    let total = 0;

    cart.forEach(i => {
        const li = document.createElement("li");
        li.innerText = `${i.name} ₹${i.price}`;
        list.appendChild(li);
        total += i.price;
    });

    document.getElementById("total").innerText = total;

    trackEvent("view_cart", { total });
}


function placeOrder() {

    const total = cart.reduce((a, b) => a + b.price, 0);

    trackEvent("order_placed", { total });

    sessionStorage.removeItem("cart");

    window.location.href = "/confirmation";
}


function confirmOrder() {
    trackEvent("order_confirmed");
}