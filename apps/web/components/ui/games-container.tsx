"use client";

import { Games } from "@/types";
import { GameCard } from "./game-card";
import { Filter } from "./filter";

interface GamesResultsProps {
  games: Games[];
  query?: string;
}

export function GamesContainer({ games }: GamesResultsProps) {
  if (games.length == 0) {
    return <div>No results</div>;
  }

  return (
    <div className="flex flex-col md:flex-row gap-6 p-6">
      <aside className="md:w-1/4 min-w-[280px] flex-shrink-0 sticky top-6 h-fit">
        <Filter></Filter>
      </aside>
      <main className="w-full">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4">
          {games.map((game) => (
            <GameCard key={game.id} game={game}></GameCard>
          ))}
        </div>
      </main>
    </div>
  );
}
