// Provider Hero UI : active les composants Hero UI dans toute l'app
'use client'; // Obligatoire pour les Providers

import { HeroUIProvider } from '@heroui/react';

export default function Providers({ children }) {
  return (
    <HeroUIProvider>
      {children}
    </HeroUIProvider>
  );
}