import Link from "next/link";
import Image from "next/image";
import logo from "@/public/logo.svg";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { cn } from "@/lib/utils";

export function Footer() {
  return (
    <footer className="bg-muted">
      <div className="w-full mx-auto max-w-screen-xl p-4 md:py-8">
        <div className="sm:flex sm:items-center sm:justify-between">
          <Link
            href="/"
            className="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse"
          >
            <Image
              className="h-7"
              src={logo}
              alt="Logo"
              width={32}
              height={32}
              style={{ width: "auto" }}
            />
            <span className="self-center text-2xl text-heading font-semibold whitespace-nowrap">
              Voxlway
            </span>
          </Link>

          <NavigationMenu>
            <NavigationMenuList className="flex flex-wrap items-center mb-6 text-sm font-medium text-body sm:mb-0">
              <NavigationMenuItem>
                <NavigationMenuLink
                  render={<Link href="/games" />}
                  className={cn(
                    navigationMenuTriggerStyle(),
                    "hover:underline me-4 md:me-6",
                  )}
                >
                  Games
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink
                  render={<Link href="" />}
                  className={cn(
                    navigationMenuTriggerStyle(),
                    "hover:underline me-4 md:me-6",
                  )}
                >
                  Features
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </div>
        <hr className="my-6 border-default sm:mx-auto lg:my-8"></hr>
        <span className="block text-sm text-body sm:text-center">
          Not affiliated with Roblox Corporation.{" "}
        </span>
      </div>
    </footer>
  );
}
