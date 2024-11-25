/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   openWizardimportXlsFile() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'file.xls',
          name:'Importer les fiches de fréquences',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
          context: {
          'form_view_ref': 'contacts_dnd.act_open_wizard_import_file_xls_frequency'
          }
      });
   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_partner.ListView.Buttons",
});
