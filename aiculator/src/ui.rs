use crate::MARGIN;
use gtk4::{
    Button, Entry, Grid,
    glib::MainContext,
    prelude::{ButtonExt, EditableExt, GridExt, GtkWindowExt},
};
use libadwaita::{Application, ApplicationWindow};

fn inverse(equation: &str) -> String {
    format!("-{}", equation)
}

fn concat(equation: &str, char: &str) -> String {
    format!("{}{}", equation, char)
}

fn button(label: &str, entry: &Entry) -> Button {
    let button = Button::builder()
        .label(label)
        .margin_top(MARGIN)
        .margin_bottom(MARGIN)
        .margin_start(MARGIN)
        .margin_end(MARGIN)
        .build();

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

    button
}

pub fn build(application: &Application) {
    let entry = Entry::builder()
        .margin_top(MARGIN)
        .margin_bottom(MARGIN)
        .margin_start(MARGIN)
        .margin_end(MARGIN)
        .build();

    let buttons = Grid::default();

    buttons.attach(&button("C", &entry), 0, 0, 10, 10);
    buttons.attach(&button("±", &entry), 10, 0, 10, 10);
    buttons.attach(&button("%", &entry), 20, 0, 10, 10);
    buttons.attach(&button("÷", &entry), 30, 0, 10, 10);

    buttons.attach(&button("7", &entry), 0, 10, 10, 10);
    buttons.attach(&button("8", &entry), 10, 10, 10, 10);
    buttons.attach(&button("9", &entry), 20, 10, 10, 10);
    buttons.attach(&button("×", &entry), 30, 10, 10, 10);

    buttons.attach(&button("4", &entry), 0, 20, 10, 10);
    buttons.attach(&button("5", &entry), 10, 20, 10, 10);
    buttons.attach(&button("6", &entry), 20, 20, 10, 10);
    buttons.attach(&button("-", &entry), 30, 20, 10, 10);

    buttons.attach(&button("1", &entry), 0, 30, 10, 10);
    buttons.attach(&button("2", &entry), 10, 30, 10, 10);
    buttons.attach(&button("3", &entry), 20, 30, 10, 10);
    buttons.attach(&button("+", &entry), 30, 30, 10, 10);

    buttons.attach(&button("0", &entry), 0, 40, 20, 10);
    buttons.attach(&button(".", &entry), 20, 40, 10, 10);
    buttons.attach(&button("=", &entry), 30, 40, 10, 10);

    let grid = Grid::builder()
        .margin_top(MARGIN)
        .margin_bottom(MARGIN)
        .margin_start(MARGIN)
        .margin_end(MARGIN)
        .build();

    grid.attach(&entry, 0, 0, 40, 10);
    grid.attach(&buttons, 0, 10, 40, 50);

    ApplicationWindow::builder()
        .application(application)
        .title("Aiculator")
        .content(&grid)
        .build()
        .present();
}
