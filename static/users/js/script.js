let leafCount = 0; // Joriy barglar soni
const maxLeaves = 20; // Maksimal barglar soni
// Snowflake yaratish funksiyasi
function createSnowflake() {
    const snowContainer = document.getElementById('snowContainer');
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');

    // Tasodifiy qor parchasi belgilari
    const snowflakeSymbols = ['❅', '❆', '✻', '✼', '✽'];
    snowflake.textContent = snowflakeSymbols[Math.floor(Math.random() * snowflakeSymbols.length)];

    // Tasodifiy o'lcham
    const size = Math.random() * 15 + 10 + 'px';
    snowflake.style.fontSize = size;

    // Tasodifiy gorizontal joylashuv
    snowflake.style.left = Math.random() * window.innerWidth + 'px';

    // Tasodifiy tushish davomiyligi
    const fallDuration = Math.random() * 5 + 3 + 's';
    snowflake.style.animationDuration = `${fallDuration}, ${Math.random() * 3 + 2}s`;

    // Tasodifiy kechikish
    const delay = Math.random() * 3 + 's';
    snowflake.style.animationDelay = `${delay}, 0s`;

    snowContainer.appendChild(snowflake);

    // Animatsiya tugaganda elementni o'chirish
    snowflake.addEventListener('animationend', () => {
        snowflake.remove();
    });
}

// Har 200ms da yangi qor qo'shish
setInterval(createSnowflake, 200);


function createRaindrop() {
    if (leafCount >= maxLeaves) {
        return;
    }
    const rainContainer = document.getElementById('rainContainer');
    const raindrop = document.createElement('div');
    raindrop.classList.add('raindrop');

    // Tasodifiy yomg'ir tomchilari belgisi
    const raindropSymbols = ['💧'];
    raindrop.textContent = raindropSymbols[Math.floor(Math.random() * raindropSymbols.length)];

    // Tasodifiy gorizontal joylashuv
    raindrop.style.left = Math.random() * window.innerWidth + 'px';

    // Tasodifiy tushish davomiyligi
    const fallDuration = Math.random() * 2 + 1 + 's';
    raindrop.style.animationDuration = fallDuration;

    // Tasodifiy kechikish
    const delay = Math.random() * 3 + 's';
    raindrop.style.animationDelay = delay;

    rainContainer.appendChild(raindrop);

    // Animatsiya tugaganda elementni o'chirish
    raindrop.addEventListener('animationend', () => {
        raindrop.remove();
    });
     // Animatsiya tugaganda elementni o'chirish
    raindrop.addEventListener('animationend', () => {
        raindrop.remove();
        leafCount--; // Har bir barg o'chirilganda sonni kamaytirish
    });

    leafCount++;
}

// Har 100ms da yangi yomg'ir tomchilarini qo'shish
setInterval(createRaindrop, 250);



function createLeafdrop() {
    if (leafCount >= maxLeaves) {
        return;
    }
    const leafContainer = document.getElementById('leafContainer');
    const leafdrop = document.createElement('div');
    leafdrop.classList.add('raindrop');

    // Tasodifiy yomg'ir tomchilari belgisi
    const leafdropSymbols = ['🍁'];
    leafdrop.textContent = leafdropSymbols[Math.floor(Math.random() * leafdropSymbols.length)];

    // Tasodifiy gorizontal joylashuv
    leafdrop.style.left = Math.random() * window.innerWidth + 'px';

    // Tasodifiy tushish davomiyligi
    const fallDuration = Math.random() * 10 + 20 + 's';
    leafdrop.style.animationDuration = fallDuration;

    // Tasodifiy kechikish
    const delay = Math.random() * 30 + 's';
    leafdrop.style.animationDelay = delay;

    leafContainer.appendChild(leafdrop);

    // Animatsiya tugaganda elementni o'chirish
    leaf.addEventListener('animationend', () => {
        leaf.remove();
        leafCount--; // Har bir barg o'chirilganda sonni kamaytirish
    });

    leafCount++; // Yangi barg qo'shilganda sonni oshirish
}

// Har 100ms da yangi yomg'ir tomchilarini qo'shish
setInterval(createLeafdrop, 900);