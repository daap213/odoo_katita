/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SelectCreateDialog } from "@web/views/view_dialogs/select_create_dialog";
import { useService } from "@web/core/utils/hooks";

/**
 * Agrega un botón "Creación masiva" en el diálogo "Buscar más..." de los
 * campos Many2one, únicamente cuando el modelo consultado es un producto.
 * Abre el asistente de creación masiva de Katita.
 */
patch(SelectCreateDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.katitaAction = useService("action");
    },

    get showKatitaMassCreate() {
        return ["product.product", "product.template"].includes(this.props.resModel);
    },

    onKatitaMassCreate() {
        this.katitaAction.doAction("katita_custom.action_katita_mass_create");
    },
});
