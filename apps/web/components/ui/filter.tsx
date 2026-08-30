"use client";

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

export function Filter() {
  return (
    <div className="bg-card border border-stroke-green shadow-xl rounded-md p-4">
      <span className="font-bold">Filters</span>
      <SearchBar className="border border-foreground"></SearchBar>
      <br></br>
      <hr className="border-default border-foreground"></hr>
      <Accordion defaultValue={["sort-by"]}>
        <AccordionItem value="sort-by">
          <AccordionTrigger className="font-bold uppercase">
            Sort By
          </AccordionTrigger>
          <AccordionContent>
            <RadioGroup defaultValue="relevance">
              <div className="flex items-center gap-3">
                <RadioGroupItem value="relevance"></RadioGroupItem>
                <Label htmlFor="r1">Relevance</Label>
              </div>
              <div className="flex items-center gap-3">
                <RadioGroupItem value="a-z"></RadioGroupItem>
                <Label htmlFor="r2">A-Z</Label>
              </div>
              <div className="flex items-center gap-3">
                <RadioGroupItem value="z-a"></RadioGroupItem>
                <Label htmlFor="r3">Z-A</Label>
              </div>
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
          <AccordionContent></AccordionContent>
        </AccordionItem>
      </Accordion>
      <hr className="border-default border-foreground"></hr>
      <Accordion>
        <AccordionItem>
          <AccordionTrigger className="font-bold uppercase">
            Tags
          </AccordionTrigger>
          <AccordionContent></AccordionContent>
        </AccordionItem>
      </Accordion>
      <hr className="border-default border-foreground pb-4"></hr>
      <Button className="w-full">Apply Filters</Button>
    </div>
  );
}
