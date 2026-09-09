"use client";

import { Games, Sort } from "@/types";
import { GameCard } from "./game-card";
import { Filter } from "./filter";
import { useEffect, useMemo, useState } from "react";

interface GamesResultsProps {
  games: Games[];
  query?: string;
}

export function GamesContainer({ games, query }: GamesResultsProps) {
  const [sort, setSort] = useState<Sort>("relevance");
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(
    new Set(),
  );
  const [selectedTags, setSelectedTags] = useState<Set<string>>(new Set());

  // Reset filters when games change
  useEffect(() => {
    setSort("relevance");
    setSelectedCategories(new Set());
    setSelectedTags(new Set());
  }, [games]);

  // Get all unique categories from the games
  const allCategories = useMemo(() => {
    const categories = games
      .map((game) => game.category)
      .filter((category): category is string => !!category);
    const sortedUniqueCategories = [...new Set(categories)].sort();
    return sortedUniqueCategories;
  }, [games]);

  // Get all unique tags from the games
  const allTags = useMemo(() => {
    const tags = games.flatMap((game) => game.tags ?? []);
    const sortedUniqueTags = [...new Set(tags)].sort();
    return sortedUniqueTags;
  }, [games]);

  // Filter and sort the games based on selected categories, tags, and sort order
  const gamesResults = useMemo(() => {
    let filteredGames = games;

    // If there are selected categories, filter to only include games that match the selected categories
    if (selectedCategories.size > 0) {
      filteredGames = filteredGames.filter(
        (game) =>
          game.category !== null && selectedCategories.has(game.category),
      );
    }

    // If there are selected tags, filter to only include games that match the selected tags
    if (selectedTags.size > 0) {
      filteredGames = filteredGames.filter((game) =>
        game.tags?.some((tag) => selectedTags.has(tag)),
      );
    }

    // If sort is by player count, sort the games in descending order of player count
    if (sort === "playerCount") {
      const sortedGames = [...filteredGames].sort(
        (a, b) => b.player_count - a.player_count,
      );
      return sortedGames;
    }

    // If sort is A-Z, sort the games alphabetically by title
    if (sort === "AToZ") {
      const sortedGames = [...filteredGames].sort((a, b) =>
        a.title.localeCompare(b.title),
      );
      return sortedGames;
    }

    // If sort is Z-A, sort the games in reverse alphabetical order by title
    if (sort === "ZToA") {
      const sortedGames = [...filteredGames].sort((a, b) =>
        b.title.localeCompare(a.title),
      );
      return sortedGames;
    }

    return filteredGames;
  }, [games, selectedCategories, selectedTags, sort]);

  // Handle category selection
  const handleCategoryChange = (category: string) => {
    setSelectedCategories((prevCategories) => {
      // Create a new Set
      const newCategories = new Set(prevCategories);

      // If the category is already selected, remove it. If not, add it
      if (newCategories.has(category)) {
        newCategories.delete(category);
      } else {
        newCategories.add(category);
      }
      return newCategories;
    });
  };

  // Handle tag selection
  const handleTagChange = (tags: string) => {
    setSelectedTags((prevTags) => {
      // Create a new Set
      const newTags = new Set(prevTags);

      // If the tag is already selected, remove it. If not, add it
      if (newTags.has(tags)) {
        newTags.delete(tags);
      } else {
        newTags.add(tags);
      }
      return newTags;
    });
  };

  // Reset all filters to their default state
  const resetFilter = () => {
    setSort("relevance");
    setSelectedCategories(new Set());
    setSelectedTags(new Set());
  };

  return (
    <div className="flex flex-col md:flex-row gap-6 p-6">
      <aside className="md:w-1/4 min-w-[280px] flex-shrink-0 sticky top-6 h-fit">
        <Filter
          query={query}
          allCategories={allCategories}
          allTags={allTags}
          selectedCategories={selectedCategories}
          selectedTags={selectedTags}
          sort={sort}
          onSortChange={setSort}
          onCategoryChange={handleCategoryChange}
          onTagChange={handleTagChange}
          resetFilter={resetFilter}
        ></Filter>
      </aside>
      <main className="w-full">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4">
          {gamesResults.map((game) => (
            <GameCard key={game.id} game={game}></GameCard>
          ))}
        </div>
      </main>
    </div>
  );
}
