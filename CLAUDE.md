# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Módulos personalizados de Odoo de Nexus-corp. La estructura clave **no está en los directorios sino en las ramas**: cada cliente tiene su propia rama de larga vida, y los addons Odoo de ese cliente viven ahí.

- `main`: solo material común al repo (LICENSE.md, README.md, configuración de herramientas). **Sin código de clientes.**
- `<version_odoo>_<cliente>`: una rama por cliente, con sus módulos personalizados. El nombre **empieza siempre por la versión de Odoo** del cliente: `19_katita` es el cliente Katita sobre Odoo 19.

Un mismo cliente puede tener varias ramas si corre (o migra a) versiones distintas de Odoo: `17_katita` y `19_katita` son ramas independientes.

Consecuencias prácticas al trabajar aquí:

- Las ramas de cliente **no se mergean** a `main` ni entre sí. No propongas un merge o PR hacia `main` para código de cliente.
- Un cliente nuevo se ramifica desde `main`, no desde otro cliente (evita arrastrar código ajeno).
- **Verifica siempre la rama activa (`git branch --show-current`) antes de editar o commitear.** El fallo más probable en este repo es dejar cambios de un cliente en `main` o en la rama de otro.
- El contenido cambia por completo entre ramas: no asumas que un archivo o módulo visto en una rama existe en otra. Explora el árbol tras cada `checkout`.
- El prefijo de la rama te dice la **versión de Odoo** contra la que se escribe el código. Respétala: la API y las vistas cambian entre versiones, así que no traslades código entre ramas de versiones distintas sin adaptarlo.

## Estado del repositorio

- `README.md` es **específico de cada rama**: en `main` documenta la convención del repo; en una rama de cliente describe a ese cliente.
- `CLAUDE.md` es **común a todas las ramas** y se mantiene idéntico: los cambios se hacen en `main` y se replican. No metas aquí detalles de un cliente concreto.
- Los módulos de cada cliente van en `addons/` de su rama (un subdirectorio por módulo, con su `__manifest__.py`); ese es el directorio que se añade al `addons_path` de la instancia.

Ramas de cliente existentes: `19_katita` (Katita sobre Odoo 19, aún sin módulos).

Aún no hay comandos de build/test/despliegue definidos en el repositorio. Cuando se adopten (cómo se levanta la instancia Odoo y cómo se corren los tests de un módulo), documéntalos aquí.

## Licencia

Software propietario y confidencial (ver LICENSE.md). No publiques, distribuyas ni copies este código fuera de Nexus-corp.
