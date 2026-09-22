# odoo_personalizado — Nexus-corp

Repositorio de **módulos personalizados de Odoo** de Nexus-corp.

## Modelo de ramas: una rama por cliente

Este repositorio **no usa ramas por feature**. La convención es:

> **Cada cliente tiene su propia rama, y en ella viven los módulos personalizados de ese cliente.**

- `main` — solo contiene lo común al repositorio (licencia, este README, `CLAUDE.md`, configuración de herramientas). No contiene código de clientes.
- `<version_odoo>_<cliente>` — una rama por cliente, con sus addons/módulos Odoo.

### Nombre de la rama

El nombre **empieza siempre por la versión de Odoo** del cliente, seguida de un guion bajo y el nombre del cliente en minúsculas:

```
19_katita     # cliente Katita sobre Odoo 19
17_acme       # cliente Acme sobre Odoo 17
```

Un mismo cliente puede tener varias ramas si corre —o está migrando— a versiones distintas de Odoo: `17_katita` y `19_katita` son ramas independientes.

Las ramas de cliente son **de larga vida**: no se mergean a `main` ni entre sí. El código de un cliente no se comparte con otro salvo que se copie de forma deliberada, y entre versiones de Odoo distintas hay que adaptarlo (la API y las vistas cambian).

## Estructura de una rama de cliente

```
addons/     # addons Odoo del cliente (un directorio por módulo, con su __manifest__.py)
```

`addons/` es el directorio que se añade al `addons_path` de la instancia Odoo del cliente.

## Trabajar con un cliente

```bash
# ver los clientes existentes
git branch -a

# empezar a trabajar con un cliente ya existente
git checkout 19_katita

# dar de alta un cliente nuevo (parte de main, no de otro cliente)
git checkout main
git checkout -b <version_odoo>_<cliente>
git push -u origin <version_odoo>_<cliente>
```

Antes de commitear, confirma en qué rama estás (`git branch --show-current`): un cambio de cliente commiteado en `main` o en la rama de otro cliente es el error más fácil de cometer aquí.

## Clientes

| Rama | Cliente | Odoo | Estado |
|---|---|---|---|
| `19_katita` | Katita | 19 | Espacio creado, sin módulos |

## Documentación compartida

`CLAUDE.md` es común a todas las ramas: se edita en `main` y se replica a las ramas de cliente. El `README.md`, en cambio, es específico de cada rama (en las de cliente describe a ese cliente).

## Licencia

Software propietario. Ver [LICENSE.md](LICENSE.md) — © 2025 Nexus-corp, todos los derechos reservados.
