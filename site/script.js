// --- Constants and Global State ---
const TRADE_GOODS_DATA = {
    "Organics": { "base_price": 17, "base_range": 0.40 },
    "Synthetics": { "base_price": 13, "base_range": 0.35 },
    "Common Minerals": { "base_price": 9, "base_range": 0.60 },
    "Rare Minerals": { "base_price": 40, "base_range": 0.50 },
    "Refined Minerals": { "base_price": 20, "base_range": 0.40 },
    "Essential Goods": { "base_price": 22, "base_range": 0.50 },
    "Medicine": { "base_price": 30, "base_range": 0.40 },
    "Vice Goods": { "base_price": 30, "base_range": 0.40 },
    "Technology Goods": { "base_price": 60, "base_range": 0.30 },
    "Luxury Goods": { "base_price": 150, "base_range": 0.25 },
    "Weapons": { "base_price": 75, "base_range": 0.33 },
    "Narcotics": { "base_price": 300, "base_range": 0.45 },
    "Equipment Parts": { "base_price": 90, "base_range": 0.15 },
    "Fuel": { "base_price": 10, "base_range": 0.30 },
    "Ammunition": { "base_price": 15, "base_range": 0.20 },
};

// Mock Player Inventory & Market State
let playerInventory = {
    "Organics": [
        { producer: "AgriCorp Zeta", quantity: 50, purchasePrice: 15 },
        { producer: "BioSphere IX", quantity: 20, purchasePrice: 16 }
    ],
    "Common Minerals": [
        { producer: "Mining Guild", quantity: 150, purchasePrice: 7 }
    ],
     "Fuel": [
        { producer: "Stellar Fuels Co.", quantity: 100, purchasePrice: 8 }
    ],
    "Medicine": [
         { producer: "Helix Pharma", quantity: 30, purchasePrice: 25 }
    ],
    "Equipment Parts": [
         { producer: "MechWorks Inc.", quantity: 15, purchasePrice: 85 }
    ]
};

let marketBuyData = {}; // { itemName: { producers: [{ name, price, quantity }], avgPrice, totalQuantity } }
let marketSellPrices = {}; // { itemName: price }

let buyCart = {}; // { uniqueId: { itemName, producerName, quantity, price, cost } }
let sellCart = {}; // { uniqueId: { itemName, inventoryIndex, stackProducer, quantity, sellPrice, purchasePrice, revenue, profit, marginPercent } }

// --- DOM Element References ---
// We get these inside init() once the DOM is ready
let buyList, sellList, buySummaryList, sellSummaryList;
let buyTotalCostEl, sellTotalRevenueEl, sellTotalProfitEl;
let confirmButton;

// --- Helper Functions ---
function formatCurrency(amount) {
    return `${Math.round(amount)}cr`;
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomFloat(min, max) {
    return Math.random() * (max - min) + min;
}

function generateProducerName() {
    const prefixes = ["Astro", "Galactic", "Stellar", "Nova", "Cosmo", "Orion", "Cygnus", "Pulsar", "Quasar", "Bio", "Terra", "Exo"];
    const mids = ["Tech", "Minerals", "Dynamics", "Logistics", "Industries", "Pharma", "Refining", "Exports", "Imports", "Foods", "Chemicals"];
    const suffixes = ["Corp", "Inc.", "Ltd.", "Syndicate", "Guild", "Co.", "Group", "Prime", "Systems", "Solutions"];
    return `${prefixes[getRandomInt(0, prefixes.length - 1)]} ${mids[getRandomInt(0, mids.length - 1)]} ${suffixes[getRandomInt(0, suffixes.length - 1)]}`;
}

// --- Market Data Generation ---
function generateMarketData() {
    marketBuyData = {};
    marketSellPrices = {};

    for (const itemName in TRADE_GOODS_DATA) {
        const basePrice = TRADE_GOODS_DATA[itemName].base_price;
        const numProducers = getRandomInt(1, 8);
        const producers = [];
        let totalQuantity = 0;
        let totalPriceSum = 0;

        for (let i = 0; i < numProducers; i++) {
            const priceMultiplier = getRandomFloat(0.8, 1.2);
            const price = Math.max(1, Math.round(basePrice * priceMultiplier));
            const quantity = getRandomInt(50, 500) * (price < basePrice ? 1.2 : 0.8); // More quantity if cheaper
            producers.push({
                name: generateProducerName(),
                price: price,
                quantity: Math.round(quantity)
            });
            totalQuantity += Math.round(quantity);
            totalPriceSum += price * Math.round(quantity);
        }

        const avgPrice = totalQuantity > 0 ? totalPriceSum / totalQuantity : basePrice;

        marketBuyData[itemName] = {
            producers: producers.sort((a,b) => a.price - b.price), // Sort producers by price
            avgPrice: Math.round(avgPrice),
            totalQuantity: totalQuantity,
            basePrice: basePrice
        };

        // Generate sell price
        marketSellPrices[itemName] = Math.max(1, Math.round(basePrice * getRandomFloat(0.65, 0.8))); // Sell price between 65%-80% of base
    }
}


// --- Populate UI Lists ---
function populateBuyList() {
    if (!buyList) return; // Ensure element exists
    buyList.innerHTML = ''; // Clear existing list/placeholder
    Object.keys(TRADE_GOODS_DATA).sort().forEach(itemName => { // Sort alphabetically
        const itemData = marketBuyData[itemName];
        if (!itemData) return;

        const li = document.createElement('li');
        li.classList.add('trade-item');
        li.dataset.itemName = itemName;
        li.dataset.type = 'buy';

        li.innerHTML = `
            <div class="item-header">
                <span class="item-icon-placeholder" data-item-name="${itemName}"></span>
                <span class="item-name">${itemName}</span>
                <button class="max-all-btn" style="display: none;" title="Set all sliders below to maximum" data-maxed="false">Max All</button>
                <button class="add-selected-btn" style="display: none;" title="Add all items with quantity > 0 below">Add Selected</button>
                <span class="item-price-info">
                    <span class="label">Avg:</span> <span class="currency">${formatCurrency(itemData.avgPrice)}</span>
                </span>
            </div>
            <div class="item-details">
                <span>Stock: ${itemData.totalQuantity.toLocaleString()} units</span>
                <span>Producers: ${itemData.producers.length}</span>
            </div>
            <div class="dropdown"></div>
        `;
        li.addEventListener('click', handleItemClick);

        // Add listeners specifically for the header buttons
        const maxAllBtn = li.querySelector('.max-all-btn');
        if (maxAllBtn) {
             maxAllBtn.addEventListener('click', handleMaxAllClick);
        }
        const addSelectedBtn = li.querySelector('.add-selected-btn');
        if (addSelectedBtn) {
             addSelectedBtn.addEventListener('click', handleAddSelectedClick);
        }

        buyList.appendChild(li);
    });
}

function populateSellList() {
     if (!sellList) return; // Ensure element exists
     sellList.innerHTML = ''; // Clear existing list/placeholder
     let sellableItems = Object.keys(playerInventory).filter(itemName =>
        playerInventory[itemName] && playerInventory[itemName].length > 0 && TRADE_GOODS_DATA[itemName]
     ).sort(); // Sort alphabetically

     if (sellableItems.length === 0) {
          sellList.innerHTML = '<li class="no-items">No items in cargo to sell.</li>';
          return;
     }

     sellableItems.forEach(itemName => {
            const basePrice = TRADE_GOODS_DATA[itemName]?.base_price;
            const sellPrice = marketSellPrices[itemName];
            if (!basePrice || !sellPrice) return; // Skip if data missing

            const totalPlayerQuantity = playerInventory[itemName].reduce((sum, stack) => sum + stack.quantity, 0);

            const li = document.createElement('li');
            li.classList.add('trade-item');
            li.dataset.itemName = itemName;
            li.dataset.type = 'sell';

            li.innerHTML = `
                <div class="item-header">
                    <span class="item-icon-placeholder" data-item-name="${itemName}"></span>
                    <span class="item-name">${itemName}</span>
                    <button class="max-all-btn" style="display: none;" title="Set all sliders below to maximum" data-maxed="false">Max All</button>
                    <button class="add-selected-btn" style="display: none;" title="Add all items with quantity > 0 below">Add Selected</button>
                    <span class="item-price-info">
                         <span class="label">Sell At:</span> <span class="currency">${formatCurrency(sellPrice)}</span>
                    </span>
                </div>
                <div class="item-details">
                    <span>In Cargo: ${totalPlayerQuantity.toLocaleString()} units</span>
                     <span>Sources: ${playerInventory[itemName].length}</span>
                </div>
                 <div class="dropdown"></div>
            `;
             li.addEventListener('click', handleItemClick);

             // Add listeners specifically for the header buttons
             const maxAllBtn = li.querySelector('.max-all-btn');
             if (maxAllBtn) {
                maxAllBtn.addEventListener('click', handleMaxAllClick);
             }
             const addSelectedBtn = li.querySelector('.add-selected-btn');
             if (addSelectedBtn) {
                  addSelectedBtn.addEventListener('click', handleAddSelectedClick);
             }

            sellList.appendChild(li);
     });
}


function handleItemClick(event) {
    // Prevent item click if header buttons were clicked directly
    if (event.target.classList.contains('max-all-btn') || event.target.classList.contains('add-selected-btn')) {
        event.stopPropagation();
        return;
    }
    // Prevent item click if clicking inside active dropdown controls
    // This allows interaction with controls without closing the dropdown via this listener
    if (event.target.closest('.dropdown-item-controls button, .dropdown-item-controls input[type="range"]')) {
        event.stopPropagation();
        return;
    }

    const clickedItem = event.currentTarget;
    const isActive = clickedItem.classList.contains('active');
    const maxAllButton = clickedItem.querySelector('.max-all-btn');
    const addSelectedButton = clickedItem.querySelector('.add-selected-btn');
    const currentDropdown = clickedItem.querySelector('.dropdown');

    if (!currentDropdown) return; // Should not happen

    // --- Logic for clicking an INACTIVE item (Opening) ---
    if (!isActive) {
        // Close all other active dropdowns first
        document.querySelectorAll('.trade-item.active').forEach(item => {
            if (item !== clickedItem) {
                item.classList.remove('active');
                const otherDropdown = item.querySelector('.dropdown');
                if (otherDropdown) {
                    otherDropdown.style.display = 'none';
                    otherDropdown.innerHTML = '';
                }
                // Hide other header buttons
                const otherMaxBtn = item.querySelector('.max-all-btn');
                const otherAddBtn = item.querySelector('.add-selected-btn');
                if(otherMaxBtn) otherMaxBtn.style.display = 'none';
                if(otherAddBtn) otherAddBtn.style.display = 'none';
            }
        });

        // Open the current dropdown
        clickedItem.classList.add('active');
        populateDropdown(clickedItem); // Build content first
        currentDropdown.style.display = 'block'; // Then display
        if(maxAllButton) maxAllButton.style.display = 'inline-block';
        if(addSelectedButton) addSelectedButton.style.display = 'inline-block';

        // Scroll the clicked item into view
        clickedItem.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            inline: 'nearest'
        });
    }
    // --- Logic for clicking an ACTIVE item (Potential Closing) ---
    else {
        // Only close if the click target is the item's header itself (or inside it)
        if (event.target.closest('.item-header')) {
             clickedItem.classList.remove('active');
             currentDropdown.style.display = 'none';
             currentDropdown.innerHTML = '';
             if(maxAllButton) maxAllButton.style.display = 'none';
             if(addSelectedButton) addSelectedButton.style.display = 'none';
        }
        // If click is inside the active item but NOT the header (e.g., item details, dropdown padding), DO NOTHING here.
        // The global listener will handle clicks outside the entire item.
    }
}

function populateDropdown(listItem) {
    const itemName = listItem.dataset.itemName;
    const type = listItem.dataset.type;
    const dropdown = listItem.querySelector('.dropdown');
    if (!dropdown) return;
    dropdown.innerHTML = ''; // Clear previous content

    if (type === 'buy') {
        const itemData = marketBuyData[itemName];
        if (!itemData || !itemData.producers) return;
        const basePrice = itemData.basePrice;

        itemData.producers.forEach((producer, index) => {
            // Unique ID for elements related to this producer
            const producerId = `buy-${itemName.replace(/[^\w]/g, '')}-${index}`;

            const div = document.createElement('div');
            div.classList.add('dropdown-item');
            div.innerHTML = `
                <div class="dd-col-price">
                    <span class="currency">${formatCurrency(producer.price)}</span>
                </div>

                <div class="dd-col-main">
                    <div class="dd-main-name">${producer.name}</div>
                    <div class="dd-main-controls">
                        <button class="dd-btn-minus" aria-label="Decrease quantity" data-target-slider="slider-${producerId}">-</button>
                        <button class="dd-btn-plus" aria-label="Increase quantity" data-target-slider="slider-${producerId}">+</button>
                        <input
                            type="range"
                            class="dd-slider"
                            id="slider-${producerId}"
                            min="0" max="${producer.quantity}" value="0"
                            data-target-display="qty-disp-${producerId}"
                            data-item-name="${itemName}"
                            data-type="buy"
                            data-producer-index="${index}"
                            data-price="${producer.price}"
                            data-producer-name="${producer.name}"
                            aria-labelledby="label-${producerId}" {/* Accessibility */}
                            >
                        <button class="max-slider-btn" title="Set max quantity" data-target-slider="slider-${producerId}">Max</button>
                    </div>
                    <span id="label-${producerId}" style="display:none;">Quantity for ${producer.name}</span>
                </div>
                <div class="dd-col-quantity" id="qty-disp-${producerId}">
                    0
                </div>
            `;
            dropdown.appendChild(div);

            // Add event listeners
            const slider = div.querySelector(`#slider-${producerId}`);
            const quantityDisplay = div.querySelector(`#qty-disp-${producerId}`); // Target new quantity display
            const minusButton = div.querySelector('.dd-btn-minus');
            const plusButton = div.querySelector('.dd-btn-plus');
            const maxButton = div.querySelector('.max-slider-btn');

            if (slider) {
                // Slider updates the quantity display in the right column
                slider.addEventListener('input', () => {
                    if (quantityDisplay) quantityDisplay.textContent = slider.value;
                });
            }
            // Use a shared handler for plus/minus
            if (minusButton) minusButton.addEventListener('click', handleQuantityAdjust);
            if (plusButton) plusButton.addEventListener('click', handleQuantityAdjust);
            // Max button still uses its specific handler
            if (maxButton) maxButton.addEventListener('click', handleMaxSliderClick);
        });

    } else if (type === 'sell') {
         const inventoryStacks = playerInventory[itemName];
         const sellPrice = marketSellPrices[itemName];
         if (!inventoryStacks || !sellPrice) return;

         inventoryStacks.forEach((stack, index) => {
              // Unique ID for elements related to this stack
              const stackId = `sell-${itemName.replace(/[^\w]/g, '')}-${index}`;

              const div = document.createElement('div');
              div.classList.add('dropdown-item');
              // NOTE: For selling, the main price shown is the SELL price,
              // while the 'bought at' price could be shown small in the middle if desired.
              // Let's show SELL price big left.
              div.innerHTML = `
                {/* Column 1: Sell Price */}
                <div class="dd-col-price">
                     <span class="currency">${formatCurrency(sellPrice)}</span>
                </div>

                {/* Column 2: Main Info & Controls */}
                 <div class="dd-col-main">
                     <div class="dd-main-name">Source: ${stack.producer} (Bought: ${formatCurrency(stack.purchasePrice)})</div>
                     <div class="dd-main-controls">
                        <button class="dd-btn-minus" aria-label="Decrease quantity" data-target-slider="slider-${stackId}">-</button>
                        <button class="dd-btn-plus" aria-label="Increase quantity" data-target-slider="slider-${stackId}">+</button>
                        <input
                            type="range"
                            class="dd-slider"
                            id="slider-${stackId}"
                            min="0" max="${stack.quantity}" value="0"
                            data-target-display="qty-disp-${stackId}"
                            data-item-name="${itemName}"
                            data-type="sell"
                            data-inventory-index="${index}"
                            data-purchase-price="${stack.purchasePrice}"
                            data-sell-price="${sellPrice}"
                            data-stack-producer="${stack.producer}"
                            aria-labelledby="label-${stackId}" {/* Accessibility */}
                            >
                        <button class="max-slider-btn" title="Set max quantity" data-target-slider="slider-${stackId}">Max</button>
                     </div>
                     {/* Hidden label for accessibility */}
                    <span id="label-${stackId}" style="display:none;">Quantity for stack from ${stack.producer}</span>
                 </div>

                 {/* Column 3: Quantity Display */}
                 <div class="dd-col-quantity" id="qty-disp-${stackId}">
                     0
                 </div>
            `;
             dropdown.appendChild(div);

             // Add event listeners
            const slider = div.querySelector(`#slider-${stackId}`);
            const quantityDisplay = div.querySelector(`#qty-disp-${stackId}`); // Target new quantity display
            const minusButton = div.querySelector('.dd-btn-minus');
            const plusButton = div.querySelector('.dd-btn-plus');
            const maxButton = div.querySelector('.max-slider-btn');

            if (slider) {
                 // Slider updates the quantity display in the right column
                 slider.addEventListener('input', () => {
                     if (quantityDisplay) quantityDisplay.textContent = slider.value;
                 });
            }
            // Use a shared handler for plus/minus
            if (minusButton) minusButton.addEventListener('click', handleQuantityAdjust);
            if (plusButton) plusButton.addEventListener('click', handleQuantityAdjust);
            // Max button still uses its specific handler
            if (maxButton) maxButton.addEventListener('click', handleMaxSliderClick);
         });
    }
}

// --- NEW Handler for +/- Buttons ---
function handleQuantityAdjust(event) {
    const button = event.target;
    const sliderId = button.dataset.targetSlider;
    const slider = document.getElementById(sliderId);

    if (!slider) return;

    const currentValue = parseInt(slider.value);
    const step = 1; // Adjust by 1
    const min = parseInt(slider.min);
    const max = parseInt(slider.max);

    let newValue = currentValue;

    if (button.classList.contains('dd-btn-plus')) {
        newValue = Math.min(max, currentValue + step); // Prevent going over max
    } else if (button.classList.contains('dd-btn-minus')) {
        newValue = Math.max(min, currentValue - step); // Prevent going under min
    }

    if (newValue !== currentValue) {
        slider.value = newValue;
        // Dispatch input event to trigger quantity display update
        slider.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

// --- Update Handler for Max Buttons (within dropdown) ---
 function handleMaxSliderClick(event) {
    const button = event.target;
    const sliderId = button.dataset.targetSlider; // Get slider ID from button
    const slider = document.getElementById(sliderId);

    if (slider) {
        slider.value = slider.max;
        // Trigger input event to update quantity display
        slider.dispatchEvent(new Event('input', { bubbles: true }));
    }
 }

 function handleMaxAllClick(event) {
    // Handles the "Max All" / "Zero All" toggle button in the item header
    event.stopPropagation(); // Prevent triggering item click
    const button = event.target;
    const tradeItem = button.closest('.trade-item');
    if (!tradeItem) return;

    const dropdown = tradeItem.querySelector('.dropdown');
    if (!dropdown) return;

    const sliders = dropdown.querySelectorAll('input[type="range"]');
    if (sliders.length === 0) return; // No sliders to process

    // Check current state using data attribute
    const isMaxed = button.dataset.maxed === 'true';

    if (isMaxed) {
        // Set all to 0
        sliders.forEach(slider => {
            slider.value = 0;
            slider.dispatchEvent(new Event('input', { bubbles: true }));
        });
        button.dataset.maxed = 'false';
        button.textContent = 'Max All';
        button.title = 'Set all sliders below to maximum';
    } else {
        // Set all to max
        sliders.forEach(slider => {
            slider.value = slider.max;
            slider.dispatchEvent(new Event('input', { bubbles: true }));
        });
        button.dataset.maxed = 'true';
        button.textContent = 'Zero All';
        button.title = 'Set all sliders below to zero';
    }
 }


// --- Handler for Add Selected Button ---
function handleAddSelectedClick(event) {
    event.stopPropagation(); // Prevent item click
    const tradeItem = event.target.closest('.trade-item');
    if (!tradeItem) return;

    const dropdown = tradeItem.querySelector('.dropdown');
    if (!dropdown) return;

    const sliders = dropdown.querySelectorAll('input[type="range"]');
    let itemsAdded = false;

    sliders.forEach(slider => {
        const quantity = parseInt(slider.value);
        if (quantity > 0) {
            itemsAdded = true;
            const dataset = slider.dataset;
            const itemName = dataset.itemName;
            const type = dataset.type;

            if (type === 'buy') {
                const producerIndex = parseInt(dataset.producerIndex); // Not strictly needed if name/price are available
                const price = parseFloat(dataset.price);
                const producerName = dataset.producerName;

                if (itemName && !isNaN(price) && producerName) {
                     // Use a unique ID for the cart item (e.g., combining item, producer, price)
                    const cartItemId = `buy-${itemName}-${producerName}-${price}`.replace(/[^\w-]+/g, '-');

                    // Add or update quantity in cart
                    if (buyCart[cartItemId]) {
                        buyCart[cartItemId].quantity += quantity;
                        buyCart[cartItemId].cost = buyCart[cartItemId].quantity * buyCart[cartItemId].price;
                    } else {
                        buyCart[cartItemId] = {
                            itemName: itemName,
                            producerName: producerName,
                            quantity: quantity,
                            price: price,
                            cost: quantity * price
                        };
                    }
                     console.log("Added/Updated Buy Cart:", cartItemId, buyCart[cartItemId]);
                } else {
                     console.warn("Missing data for buy item:", dataset);
                }

            } else if (type === 'sell') {
                const inventoryIndex = parseInt(dataset.inventoryIndex);
                const purchasePrice = parseFloat(dataset.purchasePrice);
                const sellPrice = parseFloat(dataset.sellPrice);
                const stackProducer = dataset.stackProducer;

                if (itemName && !isNaN(inventoryIndex) && !isNaN(purchasePrice) && !isNaN(sellPrice) && stackProducer) {
                     const cartItemId = `sell-${itemName}-${inventoryIndex}`; // Use index for uniqueness within sell cart

                     const revenue = quantity * sellPrice;
                     const costOfGoods = quantity * purchasePrice;
                     const profit = revenue - costOfGoods;
                     const marginPercent = costOfGoods > 0 ? (profit / costOfGoods) * 100 : (profit > 0 ? Infinity : 0);

                     // Add or update quantity in cart
                     if (sellCart[cartItemId]) {
                         sellCart[cartItemId].quantity += quantity;
                         sellCart[cartItemId].revenue = sellCart[cartItemId].quantity * sellCart[cartItemId].sellPrice;
                         sellCart[cartItemId].profit = sellCart[cartItemId].revenue - (sellCart[cartItemId].quantity * sellCart[cartItemId].purchasePrice);
                         const newCostOfGoods = sellCart[cartItemId].quantity * sellCart[cartItemId].purchasePrice;
                         sellCart[cartItemId].marginPercent = newCostOfGoods > 0 ? (sellCart[cartItemId].profit / newCostOfGoods) * 100 : (sellCart[cartItemId].profit > 0 ? Infinity : 0);
                     } else {
                        sellCart[cartItemId] = {
                            itemName: itemName,
                            inventoryIndex: inventoryIndex,
                            stackProducer: stackProducer,
                            quantity: quantity,
                            sellPrice: sellPrice,
                            purchasePrice: purchasePrice,
                            revenue: revenue,
                            profit: profit,
                            marginPercent: marginPercent
                        };
                    }
                     console.log("Added/Updated Sell Cart:", cartItemId, sellCart[cartItemId]);
                } else {
                    console.warn("Missing data for sell item:", dataset);
                }
            }

            // Reset this slider after adding its value
            slider.value = 0;
            slider.dispatchEvent(new Event('input', { bubbles: true }));
        }
    });

    if (itemsAdded) {
        updateSummary();
    }
}


// --- Update Summary Panel ---
function updateSummary() {
    if (!buySummaryList || !sellSummaryList || !buyTotalCostEl || !sellTotalRevenueEl || !sellTotalProfitEl || !confirmButton) {
        console.error("Summary panel elements not found!");
        return;
    }

    let totalBuyCost = 0;
    let totalSellRevenue = 0;
    let totalSellProfit = 0;
    let hasBuyItems = false;
    let hasSellItems = false;

    // Update Buy Summary
    buySummaryList.innerHTML = '';
    for (const id in buyCart) {
         hasBuyItems = true;
         const item = buyCart[id];
         const li = document.createElement('li');
         li.classList.add('summary-item');
         li.innerHTML = `
             <span class="summary-item-details">${item.quantity}x ${item.itemName} (from ${item.producerName})</span>
             <span class="summary-item-cost currency">${formatCurrency(item.cost)}</span>
         `;
         buySummaryList.appendChild(li);
         totalBuyCost += item.cost;
    }
     if (!hasBuyItems) { buySummaryList.innerHTML = '<li class="no-items">No items selected for purchase.</li>'; }
     buyTotalCostEl.textContent = formatCurrency(totalBuyCost);


     // Update Sell Summary
    sellSummaryList.innerHTML = '';
    for (const id in sellCart) {
        hasSellItems = true;
        const item = sellCart[id];
         const profitClass = item.profit >= 0 ? 'deal-good' : 'deal-bad';
         let marginText = '';
         if (isFinite(item.marginPercent)) {
             marginText = ` (${item.marginPercent >= 0 ? '+' : ''}${item.marginPercent.toFixed(1)}%)`;
         } else if (item.profit > 0) {
              marginText = ` (+Inf%)`; // Indicates profit with zero cost basis
         }

        const li = document.createElement('li');
        li.classList.add('summary-item');
        li.innerHTML = `
             <span class="summary-item-details">${item.quantity}x ${item.itemName} (Stack: ${item.stackProducer})</span>
             <span class="summary-item-cost">
                 <span class="currency">${formatCurrency(item.revenue)}</span>
                 (<span class="${profitClass}">${item.profit >= 0 ? '+' : ''}${formatCurrency(item.profit)}</span><span class="margin-percent">${marginText}</span>)
             </span>
        `;
        sellSummaryList.appendChild(li);
        totalSellRevenue += item.revenue;
        totalSellProfit += item.profit;
    }
     if (!hasSellItems) { sellSummaryList.innerHTML = '<li class="no-items">No items selected for sale.</li>'; }
     sellTotalRevenueEl.textContent = formatCurrency(totalSellRevenue);
     sellTotalProfitEl.textContent = formatCurrency(totalSellProfit);
     // Use classList to manage profit color more safely
     sellTotalProfitEl.classList.remove('deal-good', 'deal-bad'); // Clear previous classes
     sellTotalProfitEl.classList.add(totalSellProfit >= 0 ? 'deal-good' : 'deal-bad');


     // Enable/disable confirm button
     confirmButton.disabled = !hasBuyItems && !hasSellItems;
}

// Add close dropdown listener (only once)
function addCloseDropdownListener() {
    document.addEventListener('click', (event) => {
        const activeItem = document.querySelector('.trade-item.active');

        // If there is an active item AND the click target is NOT the active item or inside it
        if (activeItem && !activeItem.contains(event.target)) {
             // Close the active item
             activeItem.classList.remove('active');
             const dropdown = activeItem.querySelector('.dropdown');
             if (dropdown) {
                dropdown.style.display = 'none';
                dropdown.innerHTML = '';
             }
             // Also hide header buttons
             const maxAllButton = activeItem.querySelector('.max-all-btn');
             const addSelectedButton = activeItem.querySelector('.add-selected-btn');
             if(maxAllButton) maxAllButton.style.display = 'none';
             if(addSelectedButton) addSelectedButton.style.display = 'none';
         }
    }, true); // Use capture phase to catch clicks early
}


// --- Initialization ---
function init() {
    console.log("Initializing Galactic Trade Terminal...");

    // Get DOM elements now that the DOM is loaded
    buyList = document.getElementById('buy-list');
    sellList = document.getElementById('sell-list');
    buySummaryList = document.getElementById('buy-summary-list');
    sellSummaryList = document.getElementById('sell-summary-list');
    buyTotalCostEl = document.getElementById('buy-total-cost');
    sellTotalRevenueEl = document.getElementById('sell-total-revenue');
    sellTotalProfitEl = document.getElementById('sell-total-profit');
    confirmButton = document.getElementById('confirm-transaction');

    // Ensure essential elements are present before proceeding
    if (!buyList || !sellList || !buySummaryList || !sellSummaryList) {
        console.error("Critical list elements not found. Initialization aborted.");
        return;
    }

    generateMarketData();
    populateBuyList();
    populateSellList();
    updateSummary(); // Initial summary state

    // Add global listener only once
    if (!document.body.dataset.closeListenerAdded) {
        addCloseDropdownListener();
        document.body.dataset.closeListenerAdded = 'true';
    }

    console.log("Terminal Ready.");
}

// --- Run Initialization ---
// Wait for the DOM to be fully loaded before running init
document.addEventListener('DOMContentLoaded', init);