def create_payload(target, model, prompt, temperature, num_ctx, num_predict):
    return {
        "target": target,
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "num_ctx": num_ctx,
        "num_predict": num_predict
    }

def model_req(payload):
    # Fake response for testing — replace with real API call to Ollama
    import time
    start = time.time()
    response = f"Mock response for prompt: {payload['prompt']}"
    duration = round(time.time() - start, 2)
    return duration, response


