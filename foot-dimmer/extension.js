import GObject from 'gi://GObject';
import Clutter from 'gi://Clutter';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

export default class DimBackgroundWindowsExtension extends Extension {
    _DimWindowEffect = new GObject.registerClass(
        class DimWindowEffect extends Clutter.ShaderEffect {
            vfunc_get_static_shader_source() {
                return ' \
                    uniform sampler2D tex; \
                    void main() { \
                        vec4 color = texture2D(tex, cogl_tex_coord_in[0].st); \
                        color.rgb *= 0.75; \
                        cogl_color_out = color * cogl_color_in; \
                    } \
                ';
            }
        }
    );
    enable() {
        this.on_window_created = global.display.connect('window-created', this._update_on_window_created.bind(this));
    }
    _process_windows() {
        global.get_window_actors().forEach((window_actor) => {
            const target_window = window_actor.get_meta_window();
            if (target_window.get_wm_class().includes('foot')) {
                if (target_window.has_focus()) {
                    if (window_actor.get_effect('dim')) {
                        window_actor.remove_effect_by_name('dim');
                        delete window_actor._effect;
                    }
                } else if (!window_actor.get_effect('dim')) {
                    const effect = new this._DimWindowEffect();
                    window_actor._effect = effect;
                    window_actor.add_effect_with_name('dim', effect);
                }
            }
        });
    }
    _update_on_window_created(_, target_window) {
        target_window._on_focus = target_window.connect('focus', this._process_windows.bind(this));
    }
}
