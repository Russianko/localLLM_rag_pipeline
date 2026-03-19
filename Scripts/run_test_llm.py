from app.llm_client import LLMClient
from app.config import CHAT_MODEL


def main():
    llm = LLMClient()

    models = llm.get_models()
    print("Available models:")
    for model in models.data:
        print("-", model.id)

    answer = llm.ask(
        prompt="Привет! Ответь одной короткой фразой: локальная LLM подключена?",
        model=CHAT_MODEL,
    )

    print("\nModel answer:")
    print(answer)


if __name__ == "__main__":
    main()