'use client';

import { useState, useEffect, useMemo } from 'react';
import { Card, CardBody, Chip, Spinner, Divider } from '@heroui/react';

export default function FAQList() {
  const [faqData, setFaqData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFAQ = async () => {
      try {
        const res = await fetch('/api/FAQ');
        if (!res.ok) throw new Error('Erreur lors de la récupération des données');
        const data = await res.json();
        setFaqData(data.faq || data);
      } catch (err) {
        console.error('Erreur API:', err);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchFAQ();
  }, []);

  const formatCategory = (cat) =>
    cat.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase());

  const groupedFAQ = useMemo(() => {
    const groups = {};
    for (const item of faqData) {
      if (!groups[item.category]) groups[item.category] = [];
      groups[item.category].push(item);
    }
    return Object.entries(groups).sort(([a], [b]) => a.localeCompare(b, 'fr'));
  }, [faqData]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner size="lg" label="Chargement de la FAQ..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-600 font-semibold">Erreur : {error}</p>
        <p className="text-red-500 text-sm mt-2">
          Vérifiez que votre API est bien lancée.
        </p>
      </div>
    );
  }

  if (faqData.length === 0) {
    return (
      <div className="text-center py-20 text-gray-500">
        Aucune question disponible pour le moment.
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {groupedFAQ.map(([category, items]) => (
        <section key={category}>
          {/* Séparateur de catégorie */}
          <div className="flex items-center gap-4 mb-4">
            <h2 className="text-xl font-bold text-gray-800 whitespace-nowrap">
              {formatCategory(category)}
            </h2>
            <Divider className="flex-1" />
          </div>

          {/* Cartes */}
          <div className="space-y-3">
            {items.map((item) => (
              <Card
                key={item.id}
                className="bg-white shadow-md hover:shadow-lg transition-shadow"
              >
                <CardBody className="p-0">
                  <div className="flex flex-row items-stretch">
                    {/* ID à gauche, centré verticalement */}
                    <div className="flex items-center justify-center px-5 py-4 bg-gray-50 border-r border-gray-200 min-w-[80px]">
                      <Chip size="sm" variant="flat" color="default">
                        {item.id}
                      </Chip>
                    </div>

                    {/* Colonne droite : question → réponse → mots-clés */}
                    <div className="flex-1 flex flex-col gap-3 px-5 py-4">
                      <h3 className="text-base font-semibold text-gray-800">
                        {item.question}
                      </h3>

                      <Divider />

                      <p className="text-gray-700 leading-relaxed">
                        {item.answer}
                      </p>

                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {item.keywords.map((kw) => (
                          <Chip key={kw} size="sm" variant="dot" color="secondary">
                            {kw}
                          </Chip>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}