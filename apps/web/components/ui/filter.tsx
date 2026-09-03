"use client";

import { Sort } from "@/types";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "./accordion";
import { Button } from "./button";
import { Label } from "./label";
import { RadioGroup, RadioGroupItem } from "./radio-group";
import { SearchBar } from "./search";
import { FilterList } from "./filter-list";

interface FilterProps {
  query?: string;
  allCategories: string[];
  allTags: string[];
  selectedCategories: Set<string>;
  selectedTags: Set<string>;
  sort: Sort;
  onSortChange: (sort: Sort) => void;
  onCategoryChange: (category: string) => void;
  onTagChange: (tag: string) => void;
  resetFilter: () => void;
}

export function Filter({
  query,
  allCategories,
  allTags,
  selectedCategories,
  selectedTags,
  sort,
  onSortChange,
  onCategoryChange,
  onTagChange,
  resetFilter,
}: FilterProps) {
  return (
    <div className="bg-card border border-stroke-green shadow-xl rounded-md p-4">
      <div className="flex justify-between">
        <span className="font-bold">Filters</span>
        <Button
          className="bg-transparent h-auto p-0 hover:text-muted-foreground hover:bg-transparent text-foreground uppercase"
          onClick={resetFilter}
        >
          Reset
        </Button>
      </div>

      <SearchBar
        className="border border-foreground"
        initialSearchQuery={query}
      ></SearchBar>
      <br></br>
      <hr className="border-default border-foreground"></hr>
      <Accordion defaultValue={["sort-by"]}>
        <AccordionItem value="sort-by">
          <AccordionTrigger className="font-bold uppercase">
            Sort By
          </AccordionTrigger>
          <AccordionContent>
            <RadioGroup
              defaultValue={sort}
              value={sort}
              onValueChange={(value) => onSortChange(value as Sort)}
            >
              {[
                { value: "relevance", label: "Relevance" },
                { value: "playerCount", label: "Player Count" },
                { value: "AToZ", label: "A-Z" },
                { value: "ZToA", label: "Z-A" },
              ].map((o) => (
                <div className="flex items-center gap-3" key={o.value}>
                  <RadioGroupItem value={o.value} id={o.value}></RadioGroupItem>
                  <Label
                    className="hover:text-muted-foreground hover:bg-transparent text-foreground"
                    htmlFor={o.value}
                  >
                    {o.label}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <hr className="border-default border-foreground"></hr>
      <Accordion>
        <AccordionItem>
          <AccordionTrigger className="font-bold uppercase">
            Category
          </AccordionTrigger>
          <AccordionContent>
            <FilterList
              key={allCategories.join(",")}
              filterData={allCategories}
              selectedData={selectedCategories}
              onToggle={onCategoryChange}
            ></FilterList>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <hr className="border-default border-foreground"></hr>
      <Accordion>
        <AccordionItem>
          <AccordionTrigger className="font-bold uppercase">
            Tags
          </AccordionTrigger>
          <AccordionContent className="p-0">
            <FilterList
              key={allTags.join(",")}
              filterData={allTags}
              selectedData={selectedTags}
              onToggle={onTagChange}
            ></FilterList>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
