---
name: notas-de-version
description: Redacta notas de versión (release notes) a partir de una lista de cambios. Úsala cuando el usuario pida escribir el changelog o las notas de una versión del producto.
---

# Cómo redactar notas de versión

Cuando el usuario pida notas de versión, sigue este formato exacto.

## Formato de salida

```
## v<VERSIÓN> — <FECHA>

### ✨ Nuevo
- <funcionalidades nuevas, una por línea>

### 🐛 Correcciones
- <errores corregidos, uno por línea>

### ⚡ Mejoras
- <mejoras de rendimiento o experiencia, una por línea>
```

## Reglas

1. Clasifica cada cambio en una sola de las tres categorías (Nuevo, Correcciones, Mejoras).
2. Omite por completo las secciones que queden vacías.
3. Redacta cada punto en modo imperativo y orientado al usuario final (qué gana la persona, no detalles técnicos internos).
4. No inventes cambios que el usuario no haya mencionado.
5. Si el usuario no da una fecha, usa la fecha de hoy.
