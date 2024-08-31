document.addEventListener('DOMContentLoaded', () => {
    const welcomeSection = document.querySelector('.welcome-section');
    const achievementSection = document.querySelector('.achievement-section');

    // Trigger animation when the DOM is fully loaded
    setTimeout(() => {
        welcomeSection.classList.add('active-slide');
    }, 500); // Delay for the welcome section

    setTimeout(() => {
        achievementSection.classList.add('active-slide');
    }, 1500); // Delay for the achievement section
});
