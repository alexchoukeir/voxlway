import Image from "next/image";
import featuresImage from "@/public/features.webp";
import { ListFilter, Search, User } from "lucide-react";

export function Features() {
  return (
    <section
      id="features"
      className="grid min-h-[60vh] w-full place-items-center overflow-hidden"
    >
      <Image
        src={featuresImage}
        alt="Features"
        className="col-start-1 row-start-1 h-full w-full object-cover"
      />
      <div className="col-start-1 row-start-1 z-10 m-10 max-w-screen-xl bg-background rounded-2xl border border-stroke-green sm:p-10">
        <div className="text-center m-10">
          <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-5xl">
            Stop Scrolling, Start Playing
          </h1>
          <div className="flex flex-col sm:flex-row gap-4 w-full justify-center">
            <div className="flex flex-col items-center pt-10 px-10 flex-1">
              <Search className="w-15 h-15 text-stroke-green"></Search>
              <h2 className="my-4 text-2xl font-extrabold tracking-tight leading-none text-gray-900">
                Smart Search
              </h2>
              Describe the gameplay, mechanics, or vibe and get relevant results
              instantly.
            </div>
            <div className="flex flex-col items-center pt-10 px-10 flex-1">
              <ListFilter className="w-15 h-15 text-blue-400"></ListFilter>
              <h2 className="my-4 text-2xl font-extrabold tracking-tight leading-none text-gray-900">
                Deep Filtering
              </h2>
              Filter your results by category, tags, and relevancy to pinpoint
              exactly what you want to play.
            </div>
            <div className="flex flex-col items-center pt-10 px-10 flex-1">
              <User className="w-15 h-15 text-purple-400"></User>
              <h2 className="my-4 text-2xl font-extrabold tracking-tight leading-none text-gray-900">
                Built for Roblox players
              </h2>
              Voxlway was made to make discovering Roblox games easier and
              quicker.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
