import React from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@nextui-org/react";
import { UserButton } from "@clerk/nextjs";

export default function App() {
  return (
    <Navbar shouldHideOnScroll className="bg-gray-800 p-1">
      <NavbarBrand>
        <Link href="/">
          <p className="font-bold text-3xl text-inherit">tutorAI</p>
        </Link>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-10" justify="center">
        <NavbarItem isActive>
          <Link href="/home" aria-current="page">
            Home
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link href="/upload" aria-current="page">
            Upload
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link href="/chat" aria-current="page">
            Chat
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link href="/settings" aria-current="page">
            Settings
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem>
          <div style={{ transform: "scale(1.3)" }}>
            <UserButton afterSignOutUrl="/" />
          </div>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
