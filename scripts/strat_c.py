from src.utils import make_strategy_c
import time
import numpy as np
strat = make_strategy_c()

times = []

question = "Quelles sont les démarches pour déclarer une naissance ?"

for i in range(10):
    print(i)
    t0 = time.time()
    answer = strat.answer(question=question)
    times.append(time.time() - t0)
print("Réponse de l'assistant :")
print(answer)
print(np.mean(times))