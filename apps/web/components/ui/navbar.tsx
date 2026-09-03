"use client";

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
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { usePathname } from "next/dist/client/components/navigation";

export function Navbar() {
  const [isScrolling, setIsScrolling] = useState(false);
  const path = usePathname();

  useEffect(() => {
    // Handle scroll event to change navbar when scrolling
    const handleScroll = () => {
      // If the user has scrolled more than 10px, set isScrolling to true. If not, set it to false
      if (window.scrollY > 10) {
        setIsScrolling(true);
      } else {
        setIsScrolling(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    const removeScrollListener = () =>
      window.removeEventListener("scroll", handleScroll);
    return removeScrollListener;
  }, []);

  const isHomePage = path === "/";
  const isSearchPage = path.startsWith("/search");

  return (
    <header
      className={cn(
        "bg-transparent fixed w-full z-50 start-0",
        isSearchPage && "bg-background border-b top-0",
      )}
    >
      <div
        className={cn(
          "max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4 rounded-2xl transition-all duration-800 ease-in-out",
          isHomePage &&
            isScrolling &&
            "bg-navbar-background shadow-xl rounded-2xl",
        )}
      >
        <Link
          href="/"
          className="flex items-center space-x-3 rtl:space-x-reverse"
        >
          <Image
            className="h-7"
            src={logo}
            alt="Logo"
            width={32}
            height={32}
            style={{ width: "auto" }}
          />
          <span className="self-center text-xl text-heading font-semibold whitespace-nowrap">
            Voxlway
          </span>
        </Link>

        <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
          <Button>Get Started</Button>
        </div>

        <NavigationMenu className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1">
          <NavigationMenuList className="flex flex-col p-4 md:p-0 mt-4 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0">
            <NavigationMenuItem>
              <NavigationMenuLink
                render={<Link href="/games" />}
                className={cn(
                  navigationMenuTriggerStyle(),
                  "block py-2 px-3 hover:bg-neutral-tertiary",
                )}
              >
                Games
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink
                render={<Link href="#features" />}
                className={cn(
                  navigationMenuTriggerStyle(),
                  "block py-2 px-3 hover:bg-neutral-tertiary",
                )}
              >
                Features
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
    </header>
  );
}
