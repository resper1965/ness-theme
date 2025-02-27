"use client";

import { useEffect } from "react";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";

export function useInitializeEndpoint() {
  const { setSelectedEndpoint } = usePlaygroundStore();

  useEffect(() => {
    const storedEndpoint = localStorage.getItem("endpoint");

    if (!storedEndpoint) {
      localStorage.setItem("endpoint", "http://localhost:7777");
    } else if (storedEndpoint !== "http://localhost:7777") {
      setSelectedEndpoint(storedEndpoint);
    }
  }, []);
}
