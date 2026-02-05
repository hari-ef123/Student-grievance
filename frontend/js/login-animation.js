
const eyeLeft = document.querySelector('.eye-left');
const eyeRight = document.querySelector('.eye-right');
const handLeft = document.querySelector('.hand-left');
const handRight = document.querySelector('.hand-right');
const normalEyeLeft = document.querySelector('.eye-left .eye-ball');
const normalEyeRight = document.querySelector('.eye-right .eye-ball');

const usernameInput = document.querySelector('input[name="username"]');
const passwordInput = document.querySelector('input[name="password"]');

// Store original positions
let eyeLeftBounds, eyeRightBounds;

function updateBounds() {
    if (eyeLeft && eyeRight) {
        eyeLeftBounds = eyeLeft.getBoundingClientRect();
        eyeRightBounds = eyeRight.getBoundingClientRect();
    }
}

// Update bounds on resize
window.addEventListener('resize', updateBounds);
// Initial update
setTimeout(updateBounds, 500); // Wait for render

function lookAtCursor(event) {
    if (!eyeLeftBounds || !eyeRightBounds) updateBounds();
    if (!eyeLeftBounds) return; // Safety check

    const x = event.clientX;
    const y = event.clientY;

    const radianLeft = Math.atan2(y - (eyeLeftBounds.y + eyeLeftBounds.height / 2), x - (eyeLeftBounds.x + eyeLeftBounds.width / 2));
    const radianRight = Math.atan2(y - (eyeRightBounds.y + eyeRightBounds.height / 2), x - (eyeRightBounds.x + eyeRightBounds.width / 2));

    const rotationLeft = (radianLeft * (180 / Math.PI) * -1) + 180;
    const rotationRight = (radianRight * (180 / Math.PI) * -1) + 180;

    if (normalEyeLeft) normalEyeLeft.style.transform = `rotate(${rotationLeft}deg)`;
    if (normalEyeRight) normalEyeRight.style.transform = `rotate(${rotationRight}deg)`;
}

// Track mouse movement for general looking
document.addEventListener('mousemove', (e) => {
    if (document.activeElement !== passwordInput) {
        lookAtCursor(e);
    }
});

// Focus on username - strict looking
if (usernameInput) {
    usernameInput.addEventListener('focus', () => {
        if (handLeft) handLeft.classList.remove('close');
        if (handRight) handRight.classList.remove('close');
    });

    usernameInput.addEventListener('input', (e) => {
        // Could add logic to make eyes follow text caret approximately
    });
}

// Password mode - cover eyes
if (passwordInput) {
    passwordInput.addEventListener('focus', () => {
        if (handLeft) handLeft.classList.add('close');
        if (handRight) handRight.classList.add('close');
        // Reset eyes to look forward/down slightly when covered?
        // Actually, CSS handles the hands covering, JS handles the class trigger
    });

    passwordInput.addEventListener('blur', () => {
        if (handLeft) handLeft.classList.remove('close');
        if (handRight) handRight.classList.remove('close');
    });
}
