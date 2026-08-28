"use client";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useRouter } from "next/navigation";

interface SearchProps {
  initialSearchQuery?: string;
}

export function SearchBar({ initialSearchQuery = "" }: SearchProps) {
  const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
  const router = useRouter();

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const q = searchQuery.trim();

    if (!q) {
      return;
    }

    router.push(`/search?q=${encodeURIComponent(q)}`);
  }

  return (
    <form onSubmit={handleSearch}>
      <Input
        className="bg-background w-full"
        placeholder="Search..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      ></Input>
      <Button className="sr-only" type="submit"></Button>
      <Search className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground pointer-events-none"></Search>
    </form>
  );
}
