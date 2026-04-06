#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import gi

gi.require_version('Gimp', '3.0')
gi.require_version('GObject', '2.0')
from gi.repository import Gimp, GObject, GLib

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
CLIPBOARD_FILE = os.path.join(PLUGIN_DIR, "gimp_fx_clipboard.json")

class CopyPasteFx(Gimp.PlugIn):

    def do_query_procedures(self):
        return ["python-layer-fx-copy", "python-layer-fx-paste"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)

        if name == "python-layer-fx-copy":
            procedure.set_menu_label("fx Copy")
            procedure.add_menu_path("<Image>/Layer/")
            procedure.add_menu_path("<Layers>/Layers Menu")
        elif name == "python-layer-fx-paste":
            procedure.set_menu_label("fx Paste")
            procedure.add_menu_path("<Image>/Layer/")
            procedure.add_menu_path("<Layers>/Layers Menu")

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables:
            return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())

        proc_name = procedure.get_name()
        
        if proc_name == "python-layer-fx-copy":
            return self.copy_fx(drawables[0], procedure)
        elif proc_name == "python-layer-fx-paste":
            return self.paste_fx(image, drawables, procedure)

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def copy_fx(self, source_layer, procedure):
        filters = source_layer.get_filters()
        
        if not filters:
            Gimp.message("No effects found on the active layer.")
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        clipboard_data = []

        for filt in filters:
            op_name = filt.get_operation_name()
            label = op_name.split(':')[-1].replace('-', ' ').title()

            config_src = filt.get_config()
            settings = {}
            
            for prop in GObject.list_properties(config_src):
                if prop.name in ['name', 'parent', 'pointer']:
                    continue
                if prop.flags & GObject.ParamFlags.WRITABLE:
                    try:
                        val = config_src.get_property(prop.name)
                        if isinstance(val, bool):
                            settings[prop.name] = bool(val)
                        elif isinstance(val, float):
                            settings[prop.name] = float(val)
                        elif isinstance(val, int):
                            settings[prop.name] = int(val)
                        elif isinstance(val, str):
                            settings[prop.name] = str(val)
                    except:
                        pass

            clipboard_data.append({
                'op_name': op_name,
                'label': label,
                'settings': settings
            })

        try:
            with open(CLIPBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(clipboard_data, f, ensure_ascii=False, indent=4)
            Gimp.message(f"Copied {len(filters)} effect(s).")
        except Exception as e:
            Gimp.message(f"Failed to save clipboard: {e}")

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def paste_fx(self, image, targets, procedure):
        if not os.path.exists(CLIPBOARD_FILE):
            Gimp.message("No effects in memory. Please copy first.")
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        try:
            with open(CLIPBOARD_FILE, 'r', encoding='utf-8') as f:
                clipboard_data = json.load(f)
        except Exception as e:
            Gimp.message(f"Failed to load clipboard: {e}")
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        image.undo_group_start()

        try:
            for target in targets:
                # 順序を逆にしてペーストを処理する
                for fx_data in reversed(clipboard_data):
                    new_filt = Gimp.DrawableFilter.new(target, fx_data['op_name'])
                    
                    if hasattr(new_filt, 'set_label'):
                        new_filt.set_label(fx_data['label'])
                        
                    try:
                        new_filt.set_property('icon-name', 'gimp-gegl')
                    except:
                        pass

                    config_dst = new_filt.get_config()
                    error_log = []
                    
                    pspecs = {p.name: p for p in GObject.list_properties(config_dst)}
                    
                    for name, val in fx_data['settings'].items():
                        if name in pspecs:
                            v_type_name = pspecs[name].value_type.name
                            try:
                                if v_type_name in ('gdouble', 'gfloat'):
                                    cast_val = float(val)
                                elif v_type_name in ('gint', 'guint', 'gint64', 'guint64', 'glong', 'gulong'):
                                    cast_val = int(val)
                                elif v_type_name == 'gboolean':
                                    cast_val = bool(val)
                                elif v_type_name == 'gchararray':
                                    cast_val = str(val)
                                else:
                                    cast_val = val
                                    
                                config_dst.set_property(name, cast_val)
                            except Exception as e:
                                error_log.append(f"{name}: {e}")

                    if error_log:
                        print(f"[{fx_data['op_name']}] Settings Error: {', '.join(error_log)}")

                    target.append_filter(new_filt)

        except Exception as e:
            Gimp.message(f"Error: {str(e)}")
        finally:
            image.undo_group_end()
            Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == '__main__':
    Gimp.main(CopyPasteFx.__gtype__, sys.argv)