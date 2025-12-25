---
title: "Mejores Prácticas de Seguridad"
weight: 52222
---

Recomendaciones de seguridad para proteger tus claves criptográficas y keyring.

## Respaldo de Frase Semilla

La frase semilla es la única forma de recuperar tus claves. Si la pierdes, perderás acceso permanente a tus claves y, si eres validador, perderás tu validador.

### Recomendaciones

1. **Múltiples copias:** Crea al menos 2-3 copias de tu frase semilla
2. **Ubicaciones separadas:** Guarda las copias en ubicaciones físicas diferentes
3. **Resistente a desastres:** Usa materiales resistentes (papel de calidad, metal)
4. **Verificación:** Verifica que tu respaldo sea legible y completo

### Métodos de Respaldo

- **Papel:** Escribe la frase semilla en papel de calidad y guárdala en un lugar seguro
- **Metal:** Usa una solución de respaldo en metal (resistente al fuego/agua)
- **Almacenamiento encriptado:** Guarda en almacenamiento encriptado (nunca en texto plano)

### ⚠️ NUNCA

- Guardes la frase semilla en texto plano en tu computadora
- Compartas la frase semilla con nadie
- La envíes por email o mensajería
- La almacenes en la nube sin encriptar
- La fotografíes o escanees sin protección adicional

## Protección del Keyring

El keyring está protegido por una contraseña que estableces la primera vez que guardas una clave.

### Recomendaciones

1. **Contraseña fuerte:** Usa una contraseña fuerte para proteger tu keyring
   - Mínimo 12 caracteres
   - Combina mayúsculas, minúsculas, números y símbolos
   - No uses información personal o palabras comunes
2. **No compartir:** Nunca compartas tu contraseña del keyring
3. **Respaldar contraseña:** Guarda tu contraseña en un lugar seguro (separado de la frase semilla)
4. **Gestor de contraseñas:** Considera usar un gestor de contraseñas seguro

### ⚠️ ADVERTENCIA: Restablecer Contraseña del Keyring

Restablecer la contraseña del keyring crea un nuevo keyring, perdiendo acceso a todas las claves guardadas anteriormente. Solo hazlo si:
- Estás seguro de que ya no necesitas las claves guardadas anteriormente
- Tienes las frases semilla respaldadas para restaurar las claves después
- Estás empezando desde cero y no tienes claves importantes guardadas

Para más información, consulta [Restablecer Contraseña del Keyring]({{< relref "operations#restablecer-contraseña-del-keyring" >}}) en Operaciones de Gestión de Claves.

## Seguridad General

### Acceso al Servidor

1. **Acceso limitado:** Solo permite acceso al servidor a personas de confianza
2. **Autenticación fuerte:** Usa autenticación de dos factores cuando sea posible
3. **Usuarios con privilegios:** Limita el número de usuarios con acceso administrativo

### Red y Firewall

1. **Firewall configurado:** Asegúrate de que tu firewall esté correctamente configurado
2. **Puertos cerrados:** Cierra todos los puertos que no necesites
3. **VPN:** Considera usar una VPN para acceso remoto

### Mantenimiento

1. **Actualizaciones:** Mantén tu sistema y Drive actualizados
2. **Monitoreo:** Monitorea regularmente el estado de tu nodo
3. **Logs:** Revisa los logs regularmente para detectar actividad sospechosa
4. **Backups:** Realiza backups regulares de tus datos importantes

## Ver También

- [Operaciones de Gestión de Claves]({{< relref "operations" >}}) - Guía completa de todas las operaciones disponibles
- [Workflow para Validadores]({{< relref "validator-workflow" >}}) - Guía paso a paso para configurar claves como validador
- [Problemas de Gestión de Claves]({{< relref "../../../troubleshooting/key-management-issues" >}}) - Solución de problemas comunes
- [Keyring]({{< relref "../../../../../concepts/keyring" >}}) - Qué es un keyring y cómo funciona

