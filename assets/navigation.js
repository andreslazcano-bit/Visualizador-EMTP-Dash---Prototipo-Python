/**
 * ============================================================================
 * NAVEGACIÓN - MARCAR ITEMS ACTIVOS
 * ============================================================================
 * Script para marcar visualmente los items de navegación activos
 */

// Función para actualizar las clases de navegación
function updateNavigationClasses() {
    // Obtener todos los items de navegación
    const navItems = document.querySelectorAll('.list-group-item[id^="nav-"], .list-group-item[id^="sub-"]');
    
    // Función para manejar el click en un item
    function handleNavClick(event) {
        const clickedItem = event.currentTarget;
        const itemId = clickedItem.getAttribute('id');
        
        // Si es un item principal (nav-*)
        if (itemId && itemId.startsWith('nav-')) {
            // Remover clase active de todos los items principales
            document.querySelectorAll('.list-group-item[id^="nav-"]').forEach(item => {
                item.classList.remove('active');
                item.removeAttribute('aria-current');
            });
            
            // Agregar clase active al item clickeado
            clickedItem.classList.add('active');
            clickedItem.setAttribute('aria-current', 'true');
            
            // Si no es una sub-pestaña, también remover active de todas las sub-pestañas
            document.querySelectorAll('.sub-nav').forEach(subItem => {
                subItem.classList.remove('active');
                subItem.removeAttribute('aria-current');
            });
        }
        
        // Si es un sub-item (sub-*)
        if (itemId && itemId.startsWith('sub-')) {
            // Remover clase active de todos los sub-items
            document.querySelectorAll('.sub-nav').forEach(subItem => {
                subItem.classList.remove('active');
                subItem.removeAttribute('aria-current');
            });
            
            // Agregar clase active al sub-item clickeado
            clickedItem.classList.add('active');
            clickedItem.setAttribute('aria-current', 'true');
            
            // Asegurar que el item principal también esté marcado
            const parentSection = itemId.split('-')[1]; // ej: 'matricula' de 'sub-matricula-evolucion'
            const parentItem = document.getElementById(`nav-${parentSection}`);
            if (parentItem) {
                // Remover active de otros items principales
                document.querySelectorAll('.list-group-item[id^="nav-"]').forEach(item => {
                    item.classList.remove('active');
                    item.removeAttribute('aria-current');
                });
                
                parentItem.classList.add('active');
                parentItem.setAttribute('aria-current', 'true');
            }
        }
    }
    
    // Agregar event listeners a todos los items
    navItems.forEach(item => {
        item.addEventListener('click', handleNavClick);
    });
    
    // Marcar el item de inicio como activo por defecto si no hay nada activo
    const hasActiveItem = document.querySelector('.list-group-item.active');
    if (!hasActiveItem) {
        const inicioItem = document.getElementById('nav-inicio');
        if (inicioItem) {
            inicioItem.classList.add('active');
            inicioItem.setAttribute('aria-current', 'true');
        }
    }
}

// Ejecutar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateNavigationClasses);
} else {
    updateNavigationClasses();
}

// También ejecutar después de cada actualización de Dash
// (Dash re-renderiza el contenido, así que necesitamos re-aplicar los listeners)
if (window.dash_clientside) {
    window.dash_clientside = window.dash_clientside || {};
    window.dash_clientside.navigation = {
        update_active_nav: function(n_clicks, current_classes) {
            // Este es un placeholder para callbacks clientside si los necesitamos
            return current_classes;
        }
    };
}

// Usar MutationObserver para detectar cuando Dash actualiza el contenido
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            // Si se agregaron nuevos nodos, re-inicializar los event listeners
            updateNavigationClasses();
        }
    });
});

// Observar cambios en el contenedor principal
const targetNode = document.getElementById('app-container') || document.body;
observer.observe(targetNode, {
    childList: true,
    subtree: true
});
