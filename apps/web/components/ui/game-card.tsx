import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";
import Background from "@/public/background.png";
import { User } from "lucide-react";
import { Badge } from "./badge";
import { Games } from "@/types";
import Link from "next/link";
import { AspectRatio } from "./aspect-ratio";

interface GameCardProps {
  game: Games;
}

export function GameCard({ game }: GameCardProps) {
  return (
    <Link href={game.url}>
      <Card className="w-full h-full max-w-sm pt-0 border border-stroke-green shadow-xl rounded-2xl [--card-spacing:0.8rem]">
        <div className="relative w-full overflow-hidden">
          <Badge className="absolute left-3 top-3 z-10 rounded-sm px-2 py-2.5 uppercase bg-category-background text-category-foreground">
            {game.category}
          </Badge>
          <AspectRatio ratio={1 / 1}>
            <Image
              src={game.image}
              alt="text"
              className="object-cover"
              fill
              priority
            ></Image>
          </AspectRatio>
        </div>

        <CardHeader>
          <CardTitle className="font-bold">{game.title}</CardTitle>
          <CardDescription className="flex flex-row items-center gap-1">
            <User className="text-foreground w-5 h-5"></User>
            <span className="text-emerald-500">{game.player_count}</span>
          </CardDescription>
          <div className="pt-2 flex items-center gap-2 flex-wrap uppercase">
            {game.tags?.slice(0, 4).map((tag) => (
              <Badge key={tag}>{tag}</Badge>
            ))}
          </div>
        </CardHeader>
      </Card>
    </Link>
  );
}
