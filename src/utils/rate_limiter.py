"""
============================================================================
RATE LIMITER - PROTECCIÓN CONTRA FUERZA BRUTA
============================================================================
Limita intentos de login para prevenir ataques de fuerza bruta
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
from loguru import logger


class RateLimiter:
    """
    Limita intentos de login por usuario/IP
    
    Uso:
        limiter = RateLimiter(max_attempts=5, window_minutes=15)
        
        if limiter.is_allowed("admin_192.168.1.1"):
            # Permitir intento
            result = authenticate(...)
            if result:
                limiter.reset("admin_192.168.1.1")
            else:
                limiter.record_attempt("admin_192.168.1.1")
        else:
            # Bloqueado por demasiados intentos
    """
    
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        """
        Inicializa el rate limiter
        
        Args:
            max_attempts: Número máximo de intentos permitidos
            window_minutes: Ventana de tiempo en minutos
        """
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
        self.attempts: Dict[str, List[datetime]] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Verifica si se permite un intento
        
        Args:
            identifier: Identificador único (ej: "admin_IP" o "user_IP")
            
        Returns:
            True si se permite el intento, False si está bloqueado
        """
        now = datetime.now()
        
        # Limpiar intentos fuera de la ventana de tiempo
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if now - attempt < self.window
        ]
        
        # Verificar si excede el límite
        current_attempts = len(self.attempts[identifier])
        
        if current_attempts >= self.max_attempts:
            logger.warning(
                f"🚫 Rate limit excedido para: {identifier} "
                f"({current_attempts}/{self.max_attempts} intentos)"
            )
            return False
        
        return True
    
    def record_attempt(self, identifier: str):
        """
        Registra un intento fallido
        
        Args:
            identifier: Identificador único
        """
        self.attempts[identifier].append(datetime.now())
        current = len(self.attempts[identifier])
        remaining = self.max_attempts - current
        
        logger.info(
            f"📊 Intento registrado para {identifier} - "
            f"Intentos: {current}/{self.max_attempts}, Restantes: {remaining}"
        )
    
    def reset(self, identifier: str):
        """
        Resetea el contador (ej: después de login exitoso)
        
        Args:
            identifier: Identificador único
        """
        if identifier in self.attempts:
            logger.info(f"✅ Rate limit reseteado para: {identifier}")
            del self.attempts[identifier]
    
    def get_remaining_attempts(self, identifier: str) -> int:
        """
        Obtiene intentos restantes
        
        Args:
            identifier: Identificador único
            
        Returns:
            Número de intentos restantes
        """
        now = datetime.now()
        
        # Limpiar intentos antiguos
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if now - attempt < self.window
        ]
        
        current = len(self.attempts[identifier])
        return max(0, self.max_attempts - current)
    
    def get_lockout_time(self, identifier: str) -> int:
        """
        Obtiene tiempo restante de bloqueo en segundos
        
        Args:
            identifier: Identificador único
            
        Returns:
            Segundos restantes de bloqueo, 0 si no está bloqueado
        """
        if identifier not in self.attempts or not self.attempts[identifier]:
            return 0
        
        now = datetime.now()
        oldest_attempt = self.attempts[identifier][0]
        unlock_time = oldest_attempt + self.window
        
        if now < unlock_time:
            return int((unlock_time - now).total_seconds())
        
        return 0


# ============================================================================
# INSTANCIAS GLOBALES
# ============================================================================

# Rate limiter para login admin
login_limiter = RateLimiter(
    max_attempts=5,      # 5 intentos
    window_minutes=15    # en 15 minutos
)

# Rate limiter más estricto para APIs (si se implementan)
api_limiter = RateLimiter(
    max_attempts=100,    # 100 requests
    window_minutes=1     # por minuto
)


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_client_identifier(username: str, ip: str = "unknown") -> str:
    """
    Genera identificador único para rate limiting
    
    Args:
        username: Nombre de usuario
        ip: IP del cliente
        
    Returns:
        Identificador único
    """
    return f"{username}_{ip}"


def format_lockout_message(seconds: int) -> str:
    """
    Formatea mensaje de tiempo de bloqueo
    
    Args:
        seconds: Segundos restantes
        
    Returns:
        Mensaje formateado
    """
    if seconds <= 0:
        return "Ya puede intentar nuevamente"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    
    if minutes > 0:
        return f"Intente nuevamente en {minutes} minuto(s) y {remaining_seconds} segundo(s)"
    else:
        return f"Intente nuevamente en {remaining_seconds} segundo(s)"


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == '__main__':
    # Ejemplo de uso del rate limiter
    
    limiter = RateLimiter(max_attempts=3, window_minutes=1)
    identifier = "test_user_127.0.0.1"
    
    print("🧪 Probando Rate Limiter...")
    print(f"Límite: {limiter.max_attempts} intentos en {limiter.window.seconds}s\n")
    
    # Simular intentos fallidos
    for i in range(5):
        if limiter.is_allowed(identifier):
            print(f"✅ Intento {i+1}: PERMITIDO")
            limiter.record_attempt(identifier)
            remaining = limiter.get_remaining_attempts(identifier)
            print(f"   Intentos restantes: {remaining}\n")
        else:
            lockout = limiter.get_lockout_time(identifier)
            print(f"🚫 Intento {i+1}: BLOQUEADO")
            print(f"   {format_lockout_message(lockout)}\n")
    
    # Resetear
    print("🔄 Reseteando contador...")
    limiter.reset(identifier)
    
    if limiter.is_allowed(identifier):
        print("✅ Contador reseteado correctamente\n")
