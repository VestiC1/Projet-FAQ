// Layout global : structure commune à toutes les pages
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Providers from '@/components/Providers';

// Métadonnées du site (titre, description)
export const metadata = {
  title: 'Assistant FAQ',
  description: 'Interface minimaliste pour consulter la FAQ',
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body className="bg-gray-50 text-gray-900">
        {/* Provider Hero UI englobe toute l'application */}
        <Providers>
          {/* Navbar fixe en haut */}
          <Navbar />
          
          {/* Contenu principal (variable selon la page) */}
          <main className="min-h-screen pt-16 pb-20">
            {children}
          </main>
          
          {/* Footer en bas */}
          <Footer />
        </Providers>
      </body>
    </html>
  );
}