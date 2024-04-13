import React from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@nextui-org/react";

export default function App() {
  return (
    <Navbar shouldHideOnScroll className="bg-gray-800 p-1">
      <NavbarBrand>
        <Link href="/home">
          <p className="font-bold text-3xl text-inherit">tutorAI</p>
        </Link>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-10" justify="end">
        <NavbarItem isActive>
          <Link href="/sign-in" aria-current="page">
            Sign In
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link href="/sign-up" aria-current="page">
            Sign Up
          </Link>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
