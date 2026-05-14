use crate::SIZE;
use gtk4::{
    Box, Button, CssProvider, Entry, Grid, HeaderBar, Label, ListBox, Orientation,
    STYLE_PROVIDER_PRIORITY_APPLICATION, ScrolledWindow,
    gdk::Display,
    glib::MainContext,
    prelude::{BoxExt, ButtonExt, EditableExt, GridExt, GtkWindowExt, WidgetExt},
};
use libadwaita::{Application, ApplicationWindow};

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

async fn request(equation: &str, history: &ListBox) -> String {
    let response = crate::handler::request(equation).await;

    let text = if response.1 {
        format!("{} = {}", equation, response.0)
    } else {
        format!("{}", response.0)
    };
    let entry = Label::new(Some(&text));
    entry.set_xalign(0.0);
    history.append(&entry);

    response.0
}

fn add_action(label: String, button: &Button, entry: Entry, history: ListBox) {
    button.connect_clicked(move |_| {
        let entry = entry.clone();
        let history = history.clone();
        let label = label.clone();
        let text = entry.text();

        MainContext::default().spawn_local(async move {
            let text = match label.as_str() {
                "C" => String::default(),
                "=" => request(&text, &history).await,
                _ => concat(&text, &label),
            };

            entry.set_text(&text);
        });
    });
}

fn button(label: &str, entry: &Entry, history: &ListBox) -> Button {
    let button = Button::builder()
        .label(label)
        .margin_top(SIZE)
        .margin_bottom(SIZE)
        .margin_start(SIZE)
        .margin_end(SIZE)
        .build();
    button.set_hexpand(true);

    add_css(label, &button);
    add_action(label.to_string(), &button, entry.clone(), history.clone());

    button
}

pub fn build(application: &Application) {
    let s = SIZE;
    let header = HeaderBar::default();
    let history = ListBox::builder()
        .margin_top(4 * SIZE)
        .margin_bottom(2 * SIZE)
        .margin_start(4 * SIZE)
        .margin_end(4 * SIZE)
        .build();
    let entry = Entry::builder()
        .margin_top(2 * SIZE)
        .margin_bottom(2 * SIZE)
        .margin_start(4 * SIZE)
        .margin_end(4 * SIZE)
        .build();
    let buttons = Grid::builder()
        .margin_top(1 * SIZE)
        .margin_bottom(3 * SIZE)
        .margin_start(3 * SIZE)
        .margin_end(3 * SIZE)
        .build();
    let history_window = ScrolledWindow::default();
    let content = Box::new(Orientation::Vertical, 0);

    history_window.set_vexpand(true);
    history_window.set_child(Some(&history));

    buttons.attach(&button("C", &entry, &history), 0 * s, 0 * s, 1 * s, 1 * s);
    buttons.attach(&button("√", &entry, &history), 1 * s, 0 * s, 1 * s, 1 * s);
    buttons.attach(&button("^", &entry, &history), 2 * s, 0 * s, 1 * s, 1 * s);
    buttons.attach(&button("÷", &entry, &history), 3 * s, 0 * s, 1 * s, 1 * s);

    buttons.attach(&button("7", &entry, &history), 0 * s, 1 * s, 1 * s, 1 * s);
    buttons.attach(&button("8", &entry, &history), 1 * s, 1 * s, 1 * s, 1 * s);
    buttons.attach(&button("9", &entry, &history), 2 * s, 1 * s, 1 * s, 1 * s);
    buttons.attach(&button("×", &entry, &history), 3 * s, 1 * s, 1 * s, 1 * s);

    buttons.attach(&button("4", &entry, &history), 0 * s, 2 * s, 1 * s, 1 * s);
    buttons.attach(&button("5", &entry, &history), 1 * s, 2 * s, 1 * s, 1 * s);
    buttons.attach(&button("6", &entry, &history), 2 * s, 2 * s, 1 * s, 1 * s);
    buttons.attach(&button("-", &entry, &history), 3 * s, 2 * s, 1 * s, 1 * s);

    buttons.attach(&button("1", &entry, &history), 0 * s, 3 * s, 1 * s, 1 * s);
    buttons.attach(&button("2", &entry, &history), 1 * s, 3 * s, 1 * s, 1 * s);
    buttons.attach(&button("3", &entry, &history), 2 * s, 3 * s, 1 * s, 1 * s);
    buttons.attach(&button("+", &entry, &history), 3 * s, 3 * s, 1 * s, 1 * s);

    buttons.attach(&button("0", &entry, &history), 0 * s, 4 * s, 2 * s, 1 * s);
    buttons.attach(&button(".", &entry, &history), 2 * s, 4 * s, 1 * s, 1 * s);
    buttons.attach(&button("=", &entry, &history), 3 * s, 4 * s, 1 * s, 1 * s);

    content.append(&header);
    content.append(&history_window);
    content.append(&entry);
    content.append(&buttons);

    ApplicationWindow::builder()
        .application(application)
        .width_request(240)
        .height_request(426)
        .title("AIculator")
        .content(&content)
        .build()
        .present();
}
