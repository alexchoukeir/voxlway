"use client";

import { useState } from "react";
import { Checkbox } from "./checkbox";
import { Label } from "./label";
import { Button } from "./button";

interface FilterContentProps {
  filterData: string[];
  selectedData: Set<string>;
  onToggle: (data: string) => void;
}

export function FilterList({
  filterData,
  selectedData,
  onToggle,
}: FilterContentProps) {
  const [showAll, setShowAll] = useState(false);

  // If there is no filter data, return null
  if (filterData.length == 0) return null;

  return (
    <div>
      {(showAll ? filterData : filterData.slice(0, 7)).map((data) => (
        <div className="flex items-center gap-3 pb-4" key={data}>
          <Checkbox
            id={data}
            checked={selectedData.has(data)}
            onCheckedChange={() => onToggle(data)}
          ></Checkbox>
          <Label
            htmlFor={data}
            className="capitalize hover:text-muted-foreground hover:bg-transparent text-foreground"
          >
            {data}
          </Label>
        </div>
      ))}
      {filterData.length > 7 && (
        <Button
          variant="ghost"
          size="sm"
          className="bg-transparent h-auto p-0 hover:text-muted-foreground hover:bg-transparent text-foreground text-xs"
          onClick={() => setShowAll((s) => !s)}
        >
          {showAll ? "Show less" : "Show more"}
        </Button>
      )}
    </div>
  );
}
