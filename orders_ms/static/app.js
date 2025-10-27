// JavaScript para Orders Microservice Frontend

// URLs de la API
const API_BASE = 'http://localhost:8000';

// Referencias a elementos del DOM
const createOrderForm = document.getElementById('createOrderForm');
const addItemForm = document.getElementById('addItemForm');
const viewOrderForm = document.getElementById('viewOrderForm');
const orderResult = document.getElementById('orderResult');
const itemResult = document.getElementById('itemResult');
const viewOrderResult = document.getElementById('viewOrderResult');
const history = document.getElementById('history');
const clearHistoryBtn = document.getElementById('clearHistory');
const refreshOrdersBtn = document.getElementById('refreshOrdersBtn');
const refreshViewOrdersBtn = document.getElementById('refreshViewOrdersBtn');

// Variables globales
let actionHistory = JSON.parse(localStorage.getItem('orderHistory')) || [];
const PRODUCTS = { // Lista unificada de productos
    'LAPTOP123': '💻 Laptop',
    'MOUSE456': '🖱️ Mouse',
    'KEYBOARD789': '⌨️ Keyboard',
    'MONITOR147': '🖥️ Monitor',
    'MOBOARD321': 'Motherboard',
    'HEADPHONE654': '🎧 Headphones',
    'GRAPHICS987': '🎮 Graphics Card',
    'PRINTER258': '🖨️ Printer',
    'WEBCAM369': '📹 Webcam',
    'SPEAKERS159': '🔊 Speakers',
    'SSD512GBNVME': '💾 SSD 512GB',
    'RAM16GBDDR4': '🧠 RAM 16GB',
    'CPUINTELI7K': '⚙️ CPU Intel i7',
    'PSU750WGOLD': '⚡️ Power Supply 750W',
    'CASEATXMID': '🔳 PC Case ATX'
};


// Función para formatear precio con símbolo de moneda correcto
function formatPrice(amount, currency = 'EUR') {
    const symbols = {
        'EUR': '€',
        'USD': '$',
        'GBP': '£'
    };
    const symbol = symbols[currency] || '€';
    return `${amount}${symbol}`;
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    loadHistory();
    setupEventListeners();
    populateProductsDropdown();
    // Cargar órdenes automáticamente para ambos desplegables
    loadOrdersForSelect();
    loadOrdersForViewSelect();
});

// Configurar event listeners
function setupEventListeners() {
    createOrderForm.addEventListener('submit', handleCreateOrder);
    addItemForm.addEventListener('submit', handleAddItem);
    viewOrderForm.addEventListener('submit', handleViewOrder);
    clearHistoryBtn.addEventListener('click', clearHistory);
    
    // Event listener para cargar todas las órdenes
    const loadOrdersBtn = document.getElementById('loadOrdersBtn');
    if (loadOrdersBtn) {
        loadOrdersBtn.addEventListener('click', loadAllOrders);
    }
    
    // Event listener para refrescar órdenes en el desplegable
    if (refreshOrdersBtn) {
        refreshOrdersBtn.addEventListener('click', loadOrdersForSelect);
    }
    
    // Event listener para refrescar órdenes en el desplegable de view summary
    if (refreshViewOrdersBtn) {
        refreshViewOrdersBtn.addEventListener('click', loadOrdersForViewSelect);
    }
}

// Manejar creación de orden
async function handleCreateOrder(e) {
    e.preventDefault();
    
    const customerId = document.getElementById('customerId').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Deshabilitar botón mientras se procesa
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creando...';
    
    try {
        const response = await fetch(`${API_BASE}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_id: customerId
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(orderResult, `Order created successfully
                Order ID: ${data.order_id}
                Customer: ${customerId}`, 'success');
            
            // El desplegable se actualizará automáticamente con loadOrdersForSelect()
            
            // Agregar al historial
            addToHistory('Create Order', `Customer: ${customerId}`, `Order ID: ${data.order_id}`);
            
            // Refrescar ambos desplegables de órdenes
            loadOrdersForSelect();
            loadOrdersForViewSelect();
            
            // Limpiar formulario
            createOrderForm.reset();
        } else {
            showResult(orderResult, `❌ Error: ${data.detail || 'Error desconocido'}`, 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showResult(orderResult, `❌ Error de conexión: ${error.message}`, 'error');
    } finally {
        // Rehabilitar botón
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Order';
    }
}

// Manejar adición de item
async function handleAddItem(e) {
    e.preventDefault();
    
    const orderId = document.getElementById('orderId').value;
    const sku = document.getElementById('sku').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Deshabilitar botón mientras se procesa
    submitBtn.disabled = true;
    submitBtn.textContent = 'Adding...';
    
    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sku: sku,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            const productName = getProductName(sku);
            showResult(itemResult, `Item added successfully
                Product: ${productName}
                Quantity: ${quantity}
                Order: ${orderId}`, 'success');
            
            // Agregar al historial
            addToHistory('Add Item', `${productName} x${quantity}`, `Order: ${orderId}`);
            
            // Limpiar campos de producto
            document.getElementById('sku').value = '';
            document.getElementById('quantity').value = '1';
        } else {
            showResult(itemResult, `❌ ${data.message || 'Error al añadir item'}`, 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showResult(itemResult, `❌ Error de conexión: ${error.message}`, 'error');
    } finally {
        // Rehabilitar botón
        submitBtn.disabled = false;
        submitBtn.textContent = 'Add Item';
    }
}

// Manejar consulta de orden
async function handleViewOrder(e) {
    e.preventDefault();
    
    const orderId = document.getElementById('viewOrderId').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Deshabilitar botón mientras se procesa
    submitBtn.disabled = true;
    submitBtn.textContent = 'Loading...';
    
    try {
        const response = await fetch(`${API_BASE}/orders/${orderId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok && !data.error) {
            const orderSummary = formatOrderSummary(data);
            showResult(viewOrderResult, orderSummary, 'summary');

            // Expandir la card para ocupar todo el ancho
            const card = viewOrderResult.closest('.card');
            if (card) {
                card.classList.add('has-summary');
            }

            // Agregar al historial
            addToHistory('View Order', `Order ID: ${orderId}`, `${data.items_count} items - Total: ${formatPrice(data.total_amount, data.currency)}`);

            // Limpiar formulario
            viewOrderForm.reset();
        } else {
            showResult(viewOrderResult, `❌ ${data.error || data.message || 'Orden no encontrada'}`, 'error');

            // Remover la expansión de la card en caso de error
            const card = viewOrderResult.closest('.card');
            if (card) {
                card.classList.remove('has-summary');
            }
        }

    } catch (error) {
        console.error('Error:', error);
        showResult(viewOrderResult, `❌ Error de conexión: ${error.message}`, 'error');

        // Remover la expansión de la card en caso de error
        const card = viewOrderResult.closest('.card');
        if (card) {
            card.classList.remove('has-summary');
        }
    } finally {
        // Rehabilitar botón
        submitBtn.disabled = false;
        submitBtn.textContent = 'View Summary';
    }
}

// Formatear resumen de orden para mostrar
function formatOrderSummary(orderData) {
    const { order_id, customer_id, items, total_amount, items_count } = orderData;
    
    let itemsHtml = '';
    if (items && items.length > 0) {
        // Agrupar items por SKU
        const groupedItems = {};
        items.forEach(item => {
            if (groupedItems[item.sku]) {
                // Si ya existe, sumar cantidad y subtotal
                groupedItems[item.sku].quantity += item.quantity;
                groupedItems[item.sku].subtotal += item.subtotal;
            } else {
                // Si no existe, crear nueva entrada
                groupedItems[item.sku] = {
                    sku: item.sku,
                    price: item.price,
                    quantity: item.quantity,
                    subtotal: item.subtotal
                };
            }
        });

        // Generar HTML para items agrupados en grid
        const itemsArray = Object.values(groupedItems).map(item => {
            const productName = getProductName(item.sku);
            return `
                <div class="item-row">
                    <div class="item-info">
                        <div class="item-name">${productName}</div>
                        <div class="item-details">SKU: ${item.sku} | Qty: ${item.quantity}</div>
                    </div>
                    <div class="item-price">${formatPrice(item.subtotal.toFixed(2))}</div>
                </div>
            `;
        });

        itemsHtml = `<div class="items-grid">${itemsArray.join('')}</div>`;
    } else {
        itemsHtml = '<p style="text-align: center; color: #9ca3af; font-style: italic; padding: 20px;">This order has no items.</p>';
    }
    
    return `
        <div class="order-summary">
            <div class="order-header">
                <div>
                    <h3>Order: ${order_id}</h3>
                    <p>Customer: ${customer_id}</p>
                </div>
                <div class="order-total">
                    ${formatPrice(total_amount)}
                </div>
            </div>
            <div class="items-list">
                <h4>Items (${items_count})</h4>
                ${itemsHtml}
            </div>
        </div>
    `;
}

// Mostrar resultado en la UI
function showResult(element, message, type) {
    element.innerHTML = message.replace(/\n/g, '<br>');
    element.className = `result ${type}`;
    element.style.display = 'block';
    
    // Auto-ocultar después de 5 segundos solo para mensajes de éxito (no para summary)
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
    // Los mensajes tipo 'summary' y 'error' permanecen visibles hasta nueva acción
}

// Obtener nombre amigable del producto
function getProductName(sku) {
    return PRODUCTS[sku] || `📦 ${sku}`;
}

// Rellenar el desplegable de productos
function populateProductsDropdown() {
    const skuSelect = document.getElementById('sku');
    if (!skuSelect) return;

    // Limpiar opciones existentes (excepto la primera)
    skuSelect.innerHTML = '<option value="">Select a product</option>';

    for (const sku in PRODUCTS) {
        const option = document.createElement('option');
        option.value = sku;
        option.textContent = PRODUCTS[sku];
        skuSelect.appendChild(option);
    }
}

// Agregar elemento al historial
function addToHistory(action, details, result) {
    const timestamp = new Date().toLocaleString();
    const historyItem = {
        timestamp,
        action,
        details,
        result
    };
    
    actionHistory.unshift(historyItem); // Agregar al principio
    
    // Mantener solo los últimos 20 elementos
    if (actionHistory.length > 20) {
        actionHistory = actionHistory.slice(0, 20);
    }
    
    // Guardar en localStorage
    localStorage.setItem('orderHistory', JSON.stringify(actionHistory));
    
    // Actualizar UI
    loadHistory();
}

// Cargar historial en la UI
function loadHistory() {
    if (actionHistory.length === 0) {
        history.innerHTML = '<p style="text-align: center; color: #9ca3af; padding: 20px;">No actions recorded yet.</p>';
        return;
    }
    
    history.innerHTML = actionHistory.map(item => `
        <div class="history-item">
            <div class="timestamp">${item.timestamp}</div>
            <div class="action">${item.action}</div>
            <div class="details">${item.details}</div>
            <div class="details" style="color: #667eea; font-weight: 600;">${item.result}</div>
        </div>
    `).join('');
}

// Limpiar historial
function clearHistory() {
    if (confirm('Are you sure you want to clear the history?')) {
        actionHistory = [];
        localStorage.removeItem('orderHistory');
        loadHistory();
    }
}

// Cargar todas las órdenes
async function loadAllOrders() {
    const resultDiv = document.getElementById('allOrdersResult');
    const ordersList = document.getElementById('ordersList');
    
    try {
        showResult(resultDiv, 'Loading orders...', 'loading');
        
        const response = await fetch('/orders');
        const data = await response.json();
        
        if (data.error) {
            showResult(resultDiv, `Error: ${data.error}`, 'error');
            return;
        }
        
        // Mostrar órdenes
        if (data.orders && data.orders.length > 0) {
            const ordersHtml = data.orders.map(order => `
                <div class="order-item">
                    <div class="order-item-header">
                        <div class="order-id">${order.order_id}</div>
                        <div class="order-customer">Customer: ${order.customer_id}</div>
                    </div>
                    <div class="order-stats">
                        <div class="order-stat">
                            📦 Items: ${order.items_count}
                        </div>
                        <div class="order-stat order-total">
                            💰 Total: ${formatPrice(order.total_amount)}
                        </div>
                    </div>
                </div>
            `).join('');
            
            // Mostrar mensaje de éxito y lista de órdenes
            resultDiv.innerHTML = `
                <div style="background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; padding: 12px 16px; border-radius: 6px; font-size: 14px; margin-bottom: 20px;">
                    ✅ Found ${data.total_orders} orders
                </div>
                <div class="orders-list">${ordersHtml}</div>
            `;
            
            // Agregar al historial
            addToHistory(
                'Load Orders',
                'Retrieved all orders',
                `${data.total_orders} orders found`
            );
        } else {
            resultDiv.innerHTML = `
                <div style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 12px 16px; border-radius: 6px; font-size: 14px; margin-bottom: 20px;">
                    ℹ️ No orders found
                </div>
                <div class="no-orders">No orders found. Create your first order above!</div>
            `;
        }
        
    } catch (error) {
        showResult(resultDiv, `Network error: ${error.message}`, 'error');
    }
}

// Cargar órdenes para el desplegable
async function loadOrdersForSelect() {
    const orderSelect = document.getElementById('orderId');
    const refreshBtn = document.getElementById('refreshOrdersBtn');
    
    try {
        // Deshabilitar botón mientras carga
        refreshBtn.disabled = true;
        refreshBtn.textContent = '🔄 Loading...';
        
        const response = await fetch('/orders');
        const data = await response.json();
        
        // Limpiar opciones existentes
        orderSelect.innerHTML = '<option value="">Select an order</option>';
        
        if (data.orders && data.orders.length > 0) {
            // Agregar cada orden como opción
            data.orders.forEach(order => {
                const option = document.createElement('option');
                option.value = order.order_id;
                option.textContent = `${order.order_id} (${order.customer_id} - ${order.items_count} items - ${formatPrice(order.total_amount)})`;
                orderSelect.appendChild(option);
            });
            
            refreshBtn.textContent = `🔄 Loaded ${data.orders.length} orders`;
            setTimeout(() => {
                refreshBtn.textContent = '🔄 Refresh Orders';
            }, 2000);
        } else {
            orderSelect.innerHTML = '<option value="">No orders available</option>';
            refreshBtn.textContent = '🔄 No orders found';
            setTimeout(() => {
                refreshBtn.textContent = '🔄 Refresh Orders';
            }, 2000);
        }
        
    } catch (error) {
        console.error('Error loading orders for select:', error);
        orderSelect.innerHTML = '<option value="">Error loading orders</option>';
        refreshBtn.textContent = '🔄 Error';
        setTimeout(() => {
            refreshBtn.textContent = '🔄 Refresh Orders';
        }, 2000);
    } finally {
        refreshBtn.disabled = false;
    }
}

// Cargar órdenes para el desplegable de view summary
async function loadOrdersForViewSelect() {
    const viewOrderSelect = document.getElementById('viewOrderId');
    const refreshBtn = document.getElementById('refreshViewOrdersBtn');
    
    try {
        // Deshabilitar botón mientras carga
        refreshBtn.disabled = true;
        refreshBtn.textContent = '🔄 Loading...';
        
        const response = await fetch('/orders');
        const data = await response.json();
        
        // Limpiar opciones existentes
        viewOrderSelect.innerHTML = '<option value="">Select an order</option>';
        
        if (data.orders && data.orders.length > 0) {
            // Agregar cada orden como opción
            data.orders.forEach(order => {
                const option = document.createElement('option');
                option.value = order.order_id;
                option.textContent = `${order.order_id} (${order.customer_id} - ${order.items_count} items - ${formatPrice(order.total_amount)})`;
                viewOrderSelect.appendChild(option);
            });
            
            refreshBtn.textContent = `🔄 Loaded ${data.orders.length} orders`;
            setTimeout(() => {
                refreshBtn.textContent = '🔄 Refresh Orders';
            }, 2000);
        } else {
            viewOrderSelect.innerHTML = '<option value="">No orders available</option>';
            refreshBtn.textContent = '🔄 No orders found';
            setTimeout(() => {
                refreshBtn.textContent = '🔄 Refresh Orders';
            }, 2000);
        }
        
    } catch (error) {
        console.error('Error loading orders for view select:', error);
        viewOrderSelect.innerHTML = '<option value="">Error loading orders</option>';
        refreshBtn.textContent = '🔄 Error';
        setTimeout(() => {
            refreshBtn.textContent = '🔄 Refresh Orders';
        }, 2000);
    } finally {
        refreshBtn.disabled = false;
    }
}