import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";

export function SearchBar() {
  return (
    <form>
      <Input className="bg-background w-full" placeholder="Search..."></Input>
      <Search className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground pointer-events-none"></Search>
    </form>
  );
}
