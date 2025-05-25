use crate::SIZE;
use gtk4::{
    Button, CssProvider, Entry, Grid, STYLE_PROVIDER_PRIORITY_APPLICATION,
    gdk::Display,
    glib::MainContext,
    prelude::{ButtonExt, EditableExt, GridExt, GtkWindowExt, WidgetExt},
};
use libadwaita::{Application, ApplicationWindow};

fn inverse(equation: &str) -> String {
    format!("-{}", equation)
}

fn concat(equation: &str, char: &str) -> String {
    format!("{}{}", equation, char)
}

fn add_css(label: &str, button: &Button) {
    let provider = CssProvider::default();
    provider.load_from_data(
        ".raised        { background: alpha(@view_fg_color, 0.20); }
         .raised:hover  { background: alpha(@view_fg_color, 0.25); }
         .raised:active { background: alpha(@view_fg_color, 0.35); }",
    );
    gtk4::style_context_add_provider_for_display(
        &Display::default().unwrap(),
        &provider,
        STYLE_PROVIDER_PRIORITY_APPLICATION,
    );

    match label {
        "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" => button.add_css_class("raised"),
        "=" => button.add_css_class("suggested-action"),
        _ => {}
    };
}

fn add_action(label: &str, button: &Button, entry: &Entry) {
    let entry = entry.clone();
    let label = label.to_string();

    button.connect_clicked(move |_| {
        let entry = entry.clone();
        let label = label.clone();
        let text = entry.text();

        MainContext::default().spawn_local(async move {
            let text = match label.as_str() {
                "C" => String::default(),
                "±" => inverse(&text),
                "=" => crate::handler::request(&text).await,
                _ => concat(&text, &label),
            };

            entry.set_text(&text);
        });
    });
}

fn button(label: &str, entry: &Entry) -> Button {
    let button = Button::builder()
        .label(label)
        .margin_top(SIZE)
        .margin_bottom(SIZE)
        .margin_start(SIZE)
        .margin_end(SIZE)
        .build();

    add_css(label, &button);
    add_action(label, &button, &entry);

    button
}

pub fn build(application: &Application) {
    let entry = Entry::builder()
        .margin_top(4 * SIZE)
        .margin_bottom(2 * SIZE)
        .margin_start(4 * SIZE)
        .margin_end(4 * SIZE)
        .build();
    let buttons = Grid::builder()
        .margin_top(2 * SIZE - SIZE)
        .margin_bottom(4 * SIZE - SIZE)
        .margin_start(4 * SIZE - SIZE)
        .margin_end(4 * SIZE - SIZE)
        .build();
    let grid = Grid::default();

    buttons.attach(&button("C", &entry), 0 * SIZE, 0 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("±", &entry), 1 * SIZE, 0 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("%", &entry), 2 * SIZE, 0 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("÷", &entry), 3 * SIZE, 0 * SIZE, 1 * SIZE, 1 * SIZE);

    buttons.attach(&button("7", &entry), 0 * SIZE, 1 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("8", &entry), 1 * SIZE, 1 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("9", &entry), 2 * SIZE, 1 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("×", &entry), 3 * SIZE, 1 * SIZE, 1 * SIZE, 1 * SIZE);

    buttons.attach(&button("4", &entry), 0 * SIZE, 2 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("5", &entry), 1 * SIZE, 2 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("6", &entry), 2 * SIZE, 2 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("-", &entry), 3 * SIZE, 2 * SIZE, 1 * SIZE, 1 * SIZE);

    buttons.attach(&button("1", &entry), 0 * SIZE, 3 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("2", &entry), 1 * SIZE, 3 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("3", &entry), 2 * SIZE, 3 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("+", &entry), 3 * SIZE, 3 * SIZE, 1 * SIZE, 1 * SIZE);

    buttons.attach(&button("0", &entry), 0 * SIZE, 4 * SIZE, 2 * SIZE, 1 * SIZE);
    buttons.attach(&button(".", &entry), 2 * SIZE, 4 * SIZE, 1 * SIZE, 1 * SIZE);
    buttons.attach(&button("=", &entry), 3 * SIZE, 4 * SIZE, 1 * SIZE, 1 * SIZE);

    grid.attach(&entry, 0 * SIZE, 0 * SIZE, 1 * SIZE, 1 * SIZE);
    grid.attach(&buttons, 0 * SIZE, 1 * SIZE, 1 * SIZE, 1 * SIZE);

    ApplicationWindow::builder()
        .application(application)
        .width_request(1)
        .height_request(1)
        .title("Aiculator")
        .content(&grid)
        .build()
        .present();
}
