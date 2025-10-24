// Script para manejo del tema - Visualizador EMTP

// Función para aplicar tema
function applyTheme(theme) {
    const body = document.body;
    body.removeAttribute('data-theme');
    
    if (theme === 'dark') {
        body.setAttribute('data-theme', 'dark');
    }
}

// Función para detectar preferencia del sistema
function getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Inicializar tema al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Intentar obtener tema guardado
    let savedTheme;
    try {
        const stored = localStorage.getItem('_dash_theme');
        if (stored) {
            const parsed = JSON.parse(stored);
            savedTheme = parsed.theme;
        }
    } catch (e) {
        console.log('No se pudo cargar el tema guardado');
    }
    
    // Usar tema guardado o preferencia del sistema
    const theme = savedTheme || getSystemPreference();
    applyTheme(theme);
});

// Escuchar cambios en la preferencia del sistema
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    // Solo aplicar si no hay tema guardado
    try {
        const stored = localStorage.getItem('_dash_theme');
        if (!stored) {
            const theme = e.matches ? 'dark' : 'light';
            applyTheme(theme);
        }
    } catch (e) {
        const theme = e.matches ? 'dark' : 'light';
        applyTheme(theme);
    }
});