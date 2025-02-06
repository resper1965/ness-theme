import { useCallback } from "react";
import { type RunResponse } from "@/types/playground";

/**
 * Processes a single JSON chunk by passing it to the provided callback.
 * @param chunk - A parsed JSON object of type RunResponse.
 * @param onChunk - Callback to handle the chunk.
 */
function processChunk(
  chunk: RunResponse,
  onChunk: (chunk: RunResponse) => void,
) {
  onChunk(chunk);
}

/**
 * Finds the index of the closing brace ('}') for the first JSON object in the string.
 * Handles nested braces and escaped quotes.
 * @param text - The string that may contain a JSON object.
 * @returns The index of the matching '}' for the JSON object if found, or -1 if not yet complete.
 */
function findMatchingBraceEnd(text: string): number {
  let braceCount = 0;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];

    if (char === "{") {
      braceCount++;
    } else if (char === "}") {
      braceCount--;
      if (braceCount === 0) {
        // This condition is to check if the brace is end of the JSON
        return i;
      }
    }
  }
  return -1;
}

/**
 * Parses a string buffer to extract complete JSON objects.
 *
 * This function discards any extraneous data before the first '{', then
 * repeatedly finds and processes complete JSON objects.
 *
 * @param text - The accumulated string buffer.
 * @param onChunk - Callback to process each parsed JSON object.
 * @returns Remaining string that did not form a complete JSON object.
 */
function parseBuffer(
  text: string,
  onChunk: (chunk: RunResponse) => void,
): string {
  let trimmedText = text.trim(); // Remove any leading or trailing whitespace

  // Skip any non-JSON data at the beginning.
  const firstBraceIndex = trimmedText.indexOf("{");
  if (firstBraceIndex > 0) {
    trimmedText = trimmedText.slice(firstBraceIndex);
  } else if (firstBraceIndex === -1) {
    return "";
  }

  // Extract complete JSON objects as long as possible.
  while (true) {
    const objEndIndex = findMatchingBraceEnd(trimmedText);
    if (objEndIndex === -1) break;
    // Extract the candidate JSON substring.
    const JsonObject = trimmedText.slice(0, objEndIndex + 1); // Extract the complete json object from whole text
    trimmedText = trimmedText.slice(objEndIndex + 1).trim(); // Trim the text to remove the extracted json object

    try {
      const parsed = JSON.parse(JsonObject) as RunResponse;
      processChunk(parsed, onChunk);
    } catch {
      // In case the object is malformed or still incomplete,
      // break so more data can be appended.
      break;
    }
  }
  return trimmedText;
}

/**
 * Custom React hook to handle streaming API responses as JSON objects.
 *
 * This hook:
 * - Accumulates partial JSON data from streaming responses.
 * - Extracts complete JSON objects and processes them via onChunk.
 * - Handles errors via onError and signals completion with onComplete.
 *
 * @returns An object containing the streamResponse function.
 */
export default function useAIResponseStream() {
  const streamResponse = useCallback(
    async (options: {
      apiUrl: string;
      headers?: Record<string, string>;
      requestBody: FormData | Record<string, unknown>;
      onChunk: (chunk: RunResponse) => void;
      onError: (error: Error) => void;
      onComplete: () => void;
    }): Promise<void> => {
      const {
        apiUrl,
        headers = {},
        requestBody,
        onChunk,
        onError,
        onComplete,
      } = options;

      // Buffer to accumulate partial JSON data.
      let buffer = "";

      try {
        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            // Set content-type only for non-FormData requests.
            ...(!(requestBody instanceof FormData) && {
              "Content-Type": "application/json",
            }),
            ...headers,
          },
          body:
            requestBody instanceof FormData
              ? requestBody
              : JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        if (!response.body) {
          throw new Error("No response body");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        // Recursively process the stream.
        const processStream = async (): Promise<void> => {
          const { done, value } = await reader.read();
          if (done) {
            // Process any final data in the buffer.
            buffer = parseBuffer(buffer, onChunk);
            onComplete();
            return;
          }
          // Decode, sanitize, and accumulate the chunk
          buffer += decoder.decode(value, { stream: true });

          // Parse any complete JSON objects available in the buffer.
          buffer = parseBuffer(buffer, onChunk);
          await processStream();
        };
        await processStream();
      } catch (error) {
        onError(
          error instanceof Error
            ? error
            : new Error("An unknown error occurred"),
        );
      }
    },
    [],
  );

  return { streamResponse };
}
