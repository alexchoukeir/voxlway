import { Navbar } from "@/components/ui/navbar";

import { Features } from "@/components/ui/features";
import { Footer } from "@/components/ui/footer";
import { Hero } from "@/components/ui/hero";

export default function Home() {
  return (
    <div className="w-full">
      <Navbar />
      <Hero></Hero>
      <Features></Features>
      <Footer></Footer>
    </div>
  );
}
