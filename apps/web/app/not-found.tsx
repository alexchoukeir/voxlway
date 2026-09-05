import Image from "next/image";

export default function NotFound() {
  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4">
      <Image src="/404.webp" alt="Not Found" width={879} height={410} />
      <h1 className="text-2xl font-bold">
        Looks like there&apos;s nothing here
      </h1>
    </div>
  );
}
