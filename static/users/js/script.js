// const seasonEffects = document.getElementById('season-effects');

// // Faslni aniqlash
// const month = new Date().getMonth(); // 0 = Yanvar, 11 = Dekabr
// let effectType;

// if (month >= 2 && month <= 4) {
//     // Bahor
//     effectType = 'flower';
// } else if (month >= 5 && month <= 7) {
//     // Yoz
//     effectType = 'sunbeam';
// } else if (month >= 8 && month <= 10) {
//     // Kuz
//     effectType = 'leaf';
// } else {
//     // Qish
//     effectType = 'snowflake';
// }

// // Animatsiyani yaratish funksiyasi
// function createParticle() {
//     const particle = document.createElement('div');
//     particle.classList.add('particle', effectType);

//     particle.style.left = Math.random() * 100 + 'vw';
//     particle.style.animationDuration = Math.random() * 3 + 3 + 's';
//     particle.style.opacity = Math.random();

//     console.log(`Yangi ${effectType} animatsiyasi yaratildi!`); // Konsolga xabar

//     seasonEffects.appendChild(particle);

//     setTimeout(() => {
//         particle.remove();
//     }, 6000);
// }

// // Har 200ms da yangi animatsiya yaratish
// setInterval(createParticle, 200);



const snowContainer = document.getElementById('season-effects');

// Qor parchalarini yaratish funksiyasi
function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');

    // Tasodifiy joylashuv va o'lcham
    snowflake.style.left = Math.random() * 100 + 'vw';
    snowflake.style.animationDuration = Math.random() * 3 + 2 + 's'; // 2-5 soniya davomida tushadi
    snowflake.style.opacity = Math.random() * 0.5 + 0.5; // Tasodifiy shaffoflik
    snowflake.style.width = snowflake.style.height = Math.random() * 5 + 5 + 'px';

    snowContainer.appendChild(snowflake);

    // Qor parchasi tushib bo'lgandan so'ng o'chirish
    setTimeout(() => {
        snowflake.remove();
    }, 5000);
}

// Har 300ms da yangi qor parchasi yaratish
setInterval(createSnowflake, 300);
