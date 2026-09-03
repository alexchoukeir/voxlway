"use client";

import { Footer } from "@/components/ui/footer";
import { GameCardSkeleton } from "@/components/ui/game-card-skeleton";
import { GamesContainer } from "@/components/ui/games-container";
import { Navbar } from "@/components/ui/navbar";
import { Skeleton } from "@/components/ui/skeleton";
import { searchGames } from "@/lib/api";
import { Games } from "@/types";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";

  const [results, setResults] = useState<Games[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }

    setIsLoading(true);
    setError(null);

    searchGames(query)
      .then(setResults)
      .catch(() => {
        setError("Search error. Please try again later.");
        setResults([]);
      })
      .finally(() => setIsLoading(false));
  }, [query]);

  return (
    <div className="w-full pt-18">
      <div className="max-w-screen-xl mx-auto">
        {!query ? (
          <p>Search for a game</p>
        ) : isLoading ? (
          <div className="flex flex-col md:flex-row gap-6 p-6">
            <aside className="md:w-1/4 min-w-[280px] flex-shrink-0 sticky top-6 h-fit">
              <div className="bg-card border shadow-xl rounded-md p-4 flex flex-col gap-4">
                <Skeleton className="h-5 w-1/3"></Skeleton>
                <Skeleton className="h-7 w-full"></Skeleton>
                <Skeleton className="h-5 w-1/3"></Skeleton>
                <Skeleton className="h-5 w-1/2"></Skeleton>
                <Skeleton className="h-5 w-1/4"></Skeleton>
                <Skeleton className="h-5 w-1/4"></Skeleton>
                <Skeleton className="h-5 w-1/3"></Skeleton>
                <Skeleton className="h-5 w-1/3"></Skeleton>
              </div>
            </aside>
            <main className="w-full">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4">
                {Array.from({ length: 9 }).map((_, i) => (
                  <GameCardSkeleton key={i}></GameCardSkeleton>
                ))}
              </div>
            </main>
          </div>
        ) : error ? (
          <p className="text-center text-destructive">{error}</p>
        ) : (
          <GamesContainer games={results} query={query}></GamesContainer>
        )}
      </div>
    </div>
  );
}
