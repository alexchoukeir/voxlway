import Image from "next/image";
import backgroundImage from "@/public/hero.webp";
import { SearchBar } from "./search";

export function Hero() {
  return (
    <section className="relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden">
      <div className="absolute inset-0 -z-10 h-full w-full">
        <Image src={backgroundImage} alt="Background" fill />
      </div>
      <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl">
          Find the right <span className="text-stroke-green">Roblox</span> game
          faster than ever.
        </h1>
        <h2 className="mb-4">
          Search using natural language to find the next game you want to play.
        </h2>
        <div className="relative w-full">
          <SearchBar></SearchBar>
        </div>
      </div>
    </section>
  );
}
