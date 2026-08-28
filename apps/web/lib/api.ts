import { Games } from "@/types";

const API = process.env.API_URL;

export async function searchGames(query: string): Promise<Games[]> {
  const parameters = new URLSearchParams({ q: query });

  const result = await fetch(`${API}${parameters}`, {
    cache: "no-store",
  });

  if (!result.ok) {
    throw new Error(`Search error: ${result.status}`);
  }

  return result.json();
}
