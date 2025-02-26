"use client";

import { useEffect } from "react";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";

export default function EndpointInitializer() {
  const { setSelectedEndpoint } = usePlaygroundStore();

  useEffect(() => {
    // This will run only on the client side after the component mounts
    const storedEndpoint = localStorage.getItem("endpoint");

    if (!storedEndpoint) {
      // If no endpoint is stored, set the default
      localStorage.setItem("endpoint", "http://localhost:7777");
    } else if (storedEndpoint !== "http://localhost:7777") {
      // If the stored endpoint is different from the default,
      // update the store to match localStorage
      setSelectedEndpoint(storedEndpoint);
    }
  }, []); // Empty dependency array ensures this runs once after mount

  // This component doesn't render anything
  return null;
}
