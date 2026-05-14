use gtk4::gio::prelude::{ApplicationExt, ApplicationExtManual};
use libadwaita::Application;

const MODEL: &str = "tinyllama";
const SIZE: i32 = 2;

mod handler;
mod ui;

#[tokio::main]
async fn main() {
    let application = Application::default();
    application.connect_activate(ui::build);
    application.run();
}
