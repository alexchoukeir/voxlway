"use client";

import { Filter } from "@/components/ui/filter";
import { GameCard } from "@/components/ui/game-card";
import { GamesContainer } from "@/components/ui/games-container";
import { Navbar } from "@/components/ui/navbar";
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
    <div className="w-full">
      <Navbar></Navbar>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <div className="max-w-screen-xl mx-auto">
        {!query ? (
          <p>Search for a game</p>
        ) : error ? (
          <p className="text-center text-destructive">{error}</p>
        ) : (
          <GamesContainer games={results}></GamesContainer>
        )}
      </div>
    </div>
  );
}
