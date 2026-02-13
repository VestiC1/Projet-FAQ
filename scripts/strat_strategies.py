from src.utils import make_strategy_a, make_strategy_b, make_strategy_c

def test_strategy(strategy, question:str):

    print(f"\nTesting {strategy.strategy_name} ...\n")
    print("Question posée à l'assistant : ", question)
    answer = strategy.answer(question=question)
    print("Réponse de l'assistant :")
    print(answer +"\n")
    print(f"Temps écoulé : {strategy.last_ellapsed_time:.2f} secondes\n")


def main():

    print("Configuration des stratégies...")

    strat_a = make_strategy_a()
    strat_b = make_strategy_b()
    strat_c = make_strategy_c()

    strategies = [strat_a, strat_b, strat_c]

    print("Test des stratégies avec une question exemple...\n")

    question = "Quelles sont les démarches pour déclarer une naissance ?"

    for strat in strategies:
        test_strategy(strategy=strat, question=question)
        print('-' * 64)

if __name__ == "__main__":
    main()