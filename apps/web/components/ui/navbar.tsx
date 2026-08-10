"use client";

import * as React from "react";
import Link from "next/link";
import Image from "next/image";
import logo from "@/public/logo.svg";
import { Menu } from "lucide-react";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function Navbar() {
  return (
    <header className="bg-transparent fixed w-full z-50 top-0 start-0 border-b border-transparent">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <Link
          href="/"
          className="flex items-center space-x-3 rtl:space-x-reverse"
        >
          <Image className="h-7" src={logo} alt="Logo" width={32} height={32} />
          <span className="self-center text-xl text-heading font-semibold whitespace-nowrap">
            Games
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
                render={<Link href="" />}
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
