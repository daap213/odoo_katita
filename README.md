# Odoo Modul — Módulos personalizados

Repositorio de módulos personalizados para Odoo. La rama actual (`19_katita`)
contiene el módulo **`katita_custom`**, desarrollado para **Odoo 19.0**.

---

## `katita_custom` — Katita, Customizaciones

Módulo a medida para una tienda de calzado y ropa. Añade un catálogo propio de
clasificación (línea, marca, modelo, color, género), genera automáticamente un
**código de ítem** imprimible como **QR**, calcula el precio de venta a partir
del costo y permite **crear ítems masivamente** por talla o por color.

| | |
|---|---|
| **Versión** | 19.0.1.0.0 |
| **Depende de** | `product`, `stock`, `point_of_sale` |
| **Licencia** | LGPL-3 (ver `LICENSE`) |
| **Categoría** | Customizations |

### Funcionalidades

**1. Catálogo de clasificación**

Cinco modelos propios que alimentan la clasificación de cada ítem. Todos tienen
`siglas` (o `numero`) con restricción de unicidad, porque son las piezas con las
que se arma el código del producto.

| Modelo | Campo clave | Notas |
|---|---|---|
| `katita.linea` | `siglas` | Crea y mantiene sincronizada una `pos.category` propia |
| `katita.marca` | `siglas` | |
| `katita.modelo` | `siglas` | |
| `katita.color` | `siglas` | Opcional en el ítem |
| `katita.genero` | `numero` | Precargado: Masculino `01`, Femenino `02` |

La **línea** es un subconjunto de las categorías del Punto de Venta: al crearla
se genera automáticamente su `pos.category` y se agrega a los puntos de venta
que restringen categorías (`limit_categories = True`), para que sus productos
aparezcan en el POS sin configuración manual. Renombrar la línea renombra
también su categoría POS.

**2. Código de ítem y QR**

`product.template` gana el campo calculado y almacenado `katita_codigo`, que
concatena (sin separador, omitiendo lo vacío):

```
Línea.siglas + Marca.siglas + Modelo.siglas + [Color.siglas] + Género.numero + Talla
```

Ejemplo: línea `ZAP` + marca `NK` + modelo `AMX` + color `RJ` + género `01` +
talla `40` → `ZAPNKAMXRJ0140`.

El botón **Imprimir QR** en la cabecera del producto lanza el reporte
`katita_custom.action_report_katita_qr`, que renderiza el código con el
generador de códigos de barras nativo de Odoo (`widget: barcode`,
`symbology: QR`). El botón se oculta si el ítem aún no tiene código.

**3. Precio de venta calculado**

Campo `katita_price_mode` en el producto, con tres modos:

- **Precio directo** (`fixed`) — el usuario escribe el precio; es el valor por defecto.
- **% sobre costo** (`percent`) — `list_price = costo × (1 + % / 100)`.
- **Costo + valor** (`extra`) — `list_price = costo + ganancia`.

En los modos `percent` y `extra` el campo *Precio de venta* pasa a solo lectura
y se recalcula por `onchange` al cambiar el costo o los parámetros.

**4. Creación masiva de ítems**

Asistente `katita.product.mass.create`: genera varios productos independientes
(no variantes) que comparten línea, marca, modelo y género, variando por:

- **Por talla** — lista de tallas separadas por coma (`28,30,32`) y un color fijo opcional.
- **Por color** — varios colores y una talla fija.

Flujo: se llenan los datos → botón **Cargar** genera la tabla de
previsualización con nombre, color, talla, código y precio de cada ítem → botón
**Crear** los da de alta. A cada producto creado se le asigna la categoría POS
de la línea y se copia `katita_codigo` a la *Referencia interna*
(`default_code`). Al terminar se abre la lista de los ítems creados.

El asistente es accesible desde tres lugares:

- Menú **Inventario → Crear masivamente (Katita)**.
- Menú ⚙ *Acciones* de la lista o ficha de productos (acción enlazada).
- Botón **Creación masiva** dentro del diálogo *Buscar más…* de cualquier campo
  Many2one que apunte a `product.product` / `product.template` (patch OWL sobre
  `SelectCreateDialog`).

### Estructura

```
katita_custom/
├── __manifest__.py
├── data/katita_genero_data.xml          Géneros precargados (noupdate)
├── models/
│   ├── katita_catalog.py                Línea, marca, modelo, color, género
│   └── product_template.py              Código QR, modos de precio, clasificación
├── report/katita_qr_report.xml          Acción de reporte + plantilla QWeb del QR
├── security/ir.model.access.csv         Permisos por grupo
├── static/src/
│   ├── js/select_create_dialog_patch.js Botón "Creación masiva" en Buscar más…
│   └── xml/select_create_dialog.xml     Plantilla OWL heredada
├── views/
│   ├── katita_catalog_views.xml         Vistas y menús del catálogo
│   └── product_views.xml                Herencia del formulario de producto
└── wizard/
    ├── mass_create.py                   Asistente de creación masiva
    └── mass_create_views.xml            Vista, acción enlazada y menú
```

### Permisos

Definidos en `security/ir.model.access.csv`:

- **Usuarios internos** (`base.group_user`): solo lectura del catálogo.
- **Responsable de inventario** (`stock.group_stock_manager`): lectura y
  escritura del catálogo, y acceso al asistente de creación masiva.

Los menús de configuración del catálogo y el de creación masiva están
restringidos a `stock.group_stock_manager`.

### Navegación

- **Inventario → Configuración → Katita** — Líneas, Marcas, Modelos, Colores, Géneros.
- **Inventario → Crear masivamente (Katita)** — asistente.
- **Ficha de producto → pestaña Información general** — grupo *Clasificación
  Katita* y botón *Imprimir QR* en la cabecera.

---

## Instalación

1. Copiar `katita_custom/` al directorio de addons de Odoo (o agregar la ruta de
   este repositorio a `addons_path` en el archivo de configuración).
2. Reiniciar el servicio de Odoo.
3. En Odoo: activar el **modo desarrollador**, ir a **Aplicaciones**,
   *Actualizar lista de aplicaciones*, buscar «Katita» e instalar.

Ejemplo de arranque apuntando al repositorio:

```bash
odoo-bin -c odoo.conf --addons-path=/ruta/a/odoo/addons,/ruta/a/odoo_modul -d mi_base -u katita_custom
```

Tras cambios en el código, actualizar el módulo:

```bash
odoo-bin -c odoo.conf -d mi_base -u katita_custom
```

Los cambios en los assets JS/XML requieren además recargar el navegador con la
caché limpia (o arrancar con `--dev=assets`).

## Requisitos

- Odoo 19.0 (Community o Enterprise) con los módulos `product`, `stock` y
  `point_of_sale` disponibles.
- Python 3.12.
