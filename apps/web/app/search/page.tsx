"use client";

import { GameCardSkeleton } from "@/components/ui/game-card-skeleton";
import { GamesContainer } from "@/components/ui/games-container";
import { Skeleton } from "@/components/ui/skeleton";
import { searchGames } from "@/lib/api";
import { Games } from "@/types";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";

function SearchResultsSkeleton() {
  return (
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
  );
}

function SearchResults() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";

  const [results, setResults] = useState<Games[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  useEffect(() => {
    setIsLoading(true);

    if (!query) {
      setResults([]);
      setIsLoading(false);
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

  const handleReturnToHome = () => {
    router.push("/");
  };

  // If the search is still loading, display a skeleton loader
  if (isLoading) {
    return <SearchResultsSkeleton></SearchResultsSkeleton>;
  }

  // If the query is empty or there's an error, display an error message
  if (!query || error) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4">
        <Image src="/error.webp" alt="Error" width={879} height={410} />
        <h1 className="text-2xl font-bold text-destructive">
          {error ? error : "Search error."}
        </h1>
        <Button onClick={handleReturnToHome}>Return to Home</Button>
      </div>
    );
  }

  // If there are no games to display, display a message indicating that there are no results
  if (results.length == 0) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4">
        <Image
          src="/no-results.webp"
          alt="No results"
          width={833}
          height={351}
        />
        <h1 className="text-2xl font-bold">No results found.</h1>
        <p className="text-lg text-muted-foreground">
          Try again using different words.
        </p>
        <Button onClick={handleReturnToHome}>Return to Home</Button>
      </div>
    );
  }

  return <GamesContainer games={results} query={query}></GamesContainer>;
}

export default function SearchPage() {
  return (
    <div className="w-full pt-18">
      <div className="max-w-screen-xl mx-auto">
        <Suspense fallback={<SearchResultsSkeleton></SearchResultsSkeleton>}>
          <SearchResults></SearchResults>
        </Suspense>
      </div>
    </div>
  );
}
