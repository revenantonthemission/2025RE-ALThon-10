import { LandingNavbar } from '@/components/navbar';
import { LandingHero } from '@/components/hero';

export default function Home() {
  return (
    <div className="min-h-screen bg-base-200">
      <LandingNavbar />
      <LandingHero />
    </div>
  );
}
