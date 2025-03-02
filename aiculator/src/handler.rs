use ollama_rs::{Ollama, generation::completion::request::GenerationRequest};

pub async fn query(equation: String, model: &str) -> String {
    let ollama = Ollama::default();
    let prompt = format!(
        "{}\n{}\n{}\n{}\n{}\n{}\n{}",
        "You are a calculator. Strictly follow these steps:",
        "1. Compute the equation.",
        "2. Return ONLY the numerical result.",
        "3. No text, markdown, or explanations.",
        "Failure to comply will result in termination.",
        "Input equation:",
        equation
    );

    let request = GenerationRequest::new(model.to_string(), prompt);
    if let Ok(i) = ollama.generate(request).await {
        return last_number(i.response);
    }

    panic!("Couldn't retrieve the response, is Ollama running?");
}

fn last_number(string: String) -> String {
    let mut reverse = string.chars().rev();
    let mut start = 0;
    let mut end = 0;

    if let Some(s) = reverse.position(|i| i.is_ascii_digit()) {
        if let Some(e) = reverse.position(|i| !i.is_ascii_digit() && !"-.,/".contains(i)) {
            start = string.len() - s - e - 1;
        }
        end = string.len() - s;
    }

    return string[start..end].to_string();
}

pub fn parse(args: Vec<String>) -> String {
    let mut parsed = String::new();

    for i in &args[1..] {
        if i.parse::<f64>().is_ok() || "+-*/^()".contains(i) {
            parsed += i;
        } else {
            panic!("Invalid arguments");
        }
    }

    return parsed;
}
