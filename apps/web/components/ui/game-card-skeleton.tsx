import { AspectRatio } from "./aspect-ratio";
import { Card, CardHeader } from "./card";
import { Skeleton } from "./skeleton";

export function GameCardSkeleton() {
  return (
    <Card className="w-full h-full max-w-sm pt-0 shadow-xl rounded-2xl [--card-spacing:0.8rem]">
      <div className="relative w-full overflow-hidden">
        <Skeleton className="absolute left-3 top-3 z-10 rounded-sm px-2 py-2.5 h-4 w-1/2"></Skeleton>
        <AspectRatio ratio={1 / 1}>
          <Skeleton className="aspect-square w-full"></Skeleton>
        </AspectRatio>
      </div>

      <CardHeader>
        <Skeleton className="h-5 w-2/3"></Skeleton>
        <Skeleton className="h-4 w-1/3"></Skeleton>
        <div className="pt-2 flex items-center gap-2 flex-wrap">
          <Skeleton className="h-5 w-1/5"></Skeleton>
          <Skeleton className="h-5 w-1/5"></Skeleton>
          <Skeleton className="h-5 w-1/5"></Skeleton>
          <Skeleton className="h-5 w-1/5"></Skeleton>
        </div>
      </CardHeader>
    </Card>
  );
}
