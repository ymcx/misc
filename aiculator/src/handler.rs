use crate::MODEL;
use ollama_rs::{Ollama, generation::completion::request::GenerationRequest};
use regex::Regex;

pub async fn request(equation: &str) -> String {
    let equation = format!("{}=", equation);
    let request = GenerationRequest::new(MODEL.to_string(), equation);
    let response = Ollama::default().generate(request).await;

    if response.is_err() {
        return "Couldn't connect to Ollama".to_string();
    }

    let response = response.unwrap().response;
    let matches = Regex::new(r"=[^0-9+-]*([+-]?[0-9]*\.?[0-9]+)")
        .unwrap()
        .captures(&response);

    if matches.is_none() {
        return "Invalid response from Ollama".to_string();
    }

    matches.unwrap().get(1).unwrap().as_str().to_string()
}
