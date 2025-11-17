# Guía Rápida: Timeout de Sesión

## ¿Qué es el Timeout de Sesión?

Por seguridad, el sistema cierra automáticamente tu sesión después de **30 minutos de inactividad**. Esto previene el acceso no autorizado si dejas tu computador desatendido.

## ¿Qué cuenta como "actividad"?

El sistema detecta que estás activo cuando:
- Navegas entre diferentes páginas
- Cambias de pestaña en el menú lateral
- Interactúas con filtros, botones o gráficos
- Haces clic en cualquier parte de la aplicación

## ¿Qué pasa cuando expira mi sesión?

### Si entraste como "Usuario" (sin contraseña)

Verás un mensaje amigable que dice:

```
Sesión Expirada

Tu sesión ha expirado por inactividad.

Por motivos de seguridad, las sesiones se cierran 
automáticamente después de 30 minutos sin actividad.

[Volver al Inicio]
```

Solo necesitas hacer clic en "Volver al Inicio" y entrar nuevamente.

### Si entraste como "Admin", "Analista", "Editor" o "Viewer" (con contraseña)

Verás un mensaje diferente:

```
Re-autenticación Requerida

Tu sesión ha expirado por inactividad. 
Por favor, ingresa tu contraseña para continuar.

Contraseña: [____________]

[Volver al Inicio]  [Continuar]
```

**Opciones:**
1. **Continuar trabajando**: Ingresa tu contraseña y haz clic en "Continuar"
   - ✅ Si la contraseña es correcta, sigues trabajando donde estabas
   - ❌ Si es incorrecta, debes volver a iniciar sesión

2. **Volver al inicio**: Haz clic en "Volver al Inicio"
   - Vuelves a la pantalla de bienvenida
   - Debes entrar nuevamente seleccionando tu modo

## ¿Cómo evitar que expire mi sesión?

**Simple**: Solo mantente activo. 

Si estás trabajando activamente (navegando, filtrando datos, viendo gráficos), tu sesión se mantiene activa automáticamente.

Si necesitas alejarte del computador:
- **Menos de 30 minutos**: No hay problema, puedes volver y seguir trabajando
- **Más de 30 minutos**: Tu sesión expirará, pero es fácil volver a entrar

## ¿Por qué existe esta función?

**Seguridad**. Esta función protege:
- Tus datos personales
- La información sensible del sistema
- El acceso de usuarios no autorizados

Es especialmente importante en:
- Computadores compartidos
- Oficinas con acceso público
- Equipos que pueden quedar desatendidos

## ¿Cuándo se me advierte?

**Actualmente**: Solo recibes el mensaje cuando ya expiró la sesión.

**Próximamente** (mejora futura): Recibirás una advertencia 5 minutos antes de que expire, con opción de extender la sesión.

## Preguntas Frecuentes

### ¿Pierdo mi trabajo si expira la sesión?
No. Los datos que estabas viendo no se pierden. Solo necesitas volver a entrar.

### ¿Puedo cambiar el tiempo de 30 minutos?
Si eres administrador del sistema, sí. Se puede configurar en el archivo `.env` modificando la variable `SESSION_TIMEOUT_MINUTES`.

### ¿Qué pasa si estoy viendo un gráfico sin hacer clic?
Si solo estás mirando la pantalla sin interactuar durante más de 30 minutos, la sesión expirará. Necesitas hacer alguna interacción (cambiar filtro, cambiar pestaña, etc.) para mantenerla activa.

### ¿La sesión expira si cierro el navegador?
Sí. Al cerrar el navegador, la sesión se cierra automáticamente. Deberás entrar nuevamente cuando vuelvas a abrir la aplicación.

### ¿Puedo tener varias sesiones abiertas?
Sí, puedes abrir la aplicación en varias pestañas o navegadores. Cada una tiene su propia sesión independiente.

## Contacto

Si tienes problemas o preguntas sobre el sistema de timeout:

**Email**: ext.andres.lazcano@mineduc.cl

---

**Última actualización**: 17 de Noviembre 2025
