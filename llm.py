from transformers import T5ForConditionalGeneration, T5Tokenizer
from logger import logger

_model = None
_tokenizer = None


def get_generator():
    global _model, _tokenizer
    if _model is None:
        logger.info("Loading LLM (google/flan-t5-small)")
        _tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        _model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
    return _model, _tokenizer


def generate_answer(context, question):
    model, tokenizer = get_generator()

    # Improved prompt for Flan-T5 to encourage more detailed answers
    prompt = f"""Answer the following question in a detailed, informative, and professional way using the provided research paper context.

Context:
{context}

Question: {question}

Detailed Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
    
    # Adjusted parameters for better generation
    outputs = model.generate(
        inputs["input_ids"],
        max_new_tokens=256,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Cleanup if the model starts with "Answer:" or similar artifacts
    if answer.lower().startswith("answer:"):
        answer = answer[7:].strip()
        
    return answer.strip()