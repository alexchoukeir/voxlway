export interface Games {
  id: number;
  external_id: number;
  title: string;
  player_count: number;
  url: string;
  image: string;
  category: string | null;
  tags: string[] | null;
  similarity: number;
}
