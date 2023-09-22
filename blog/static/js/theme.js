tailwind.config = {
    darkMode: 'class',
}

const html = document.querySelector('html');
const darkModeBtn = document.querySelector('a[data-theme-mode="dark"]');
const lightModeBtn = document.querySelector('a[data-theme-mode="light"]');
const themeMode = localStorage.getItem('themeMode') === null ? 'light' : localStorage.getItem('themeMode');

function switchToDarkMode() {
html.classList.add('dark');
html.classList.remove('light');
darkModeBtn.style.display = 'none';
lightModeBtn.style.display = 'inline-block';
localStorage.setItem('themeMode', 'dark');
}

function switchToLightMode() {
html.classList.add('light');
html.classList.remove('dark');
lightModeBtn.style.display = 'none';
darkModeBtn.style.display = 'inline-block';
localStorage.setItem('themeMode', 'light');
}

if (themeMode === 'dark') {
switchToDarkMode();
} else if (themeMode === 'light') {
switchToLightMode();
}

darkModeBtn.addEventListener('click', switchToDarkMode);
lightModeBtn.addEventListener('click', switchToLightMode);
