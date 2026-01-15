from src.llm import LLMChatCompletion
from config import HF_TOKEN, LLMNAME, DATA_DIR
from scripts.data_loader import load_golden
import json
def main():
    system_prompt = """
    Tu es un assistant IA français dédié à répondre aux questions administratives pour la Communauté de Communes Val de Loire Numérique.
    Réponds aux questions des citoyens **uniquement** avec les informations que tu possèdes déjà.
    Si tu ne connais pas la réponse, dis : "Je n’ai pas d’information sur ce sujet. Contactez un agent."

    **Règles :**
    - Langue : français uniquement.
    - Format : simple court et informatif.
    - Pas d’hallucinations : si incertain, considère que tu ne connais pas.
    - Périmètre : état civil, urbanisme, déchets, transports, petite-enfance, social, vie associative, élections, logement, culture/sport, fiscalité, eau/assainissement.
    - Si c'est hors périmètre considère que tu ne connais pas
    """

    llm = LLMChatCompletion(system_prompt=system_prompt, max_tokens=200)

    #result = llm.reply(prompt="Quelles sont les démarches pour déclarer une naissance ?")
    print()
    #print(result)

    answers = []
    golden_data = load_golden()['golden_set']
    for item in golden_data:
        q = item['question']
        print("Q:", q)
        result = llm.reply(prompt=q)
        print("A:", result)
        answers.append({
            'question': q,
            'answer': str(result)
        })
    with open(DATA_DIR / 'llm_answers.json', 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
