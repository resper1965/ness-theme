import { type ReactNode } from "react";

import { formatDate } from "./format";

export type Code = string | object | ReactNode;

export const parseUrl = (urlString: string): string => {
  let modifiedString = urlString.replace(/:$/, "");

  try {
    if (!/^[a-zA-Z]+:\/\//.test(modifiedString)) {
      modifiedString = `http://${modifiedString}`;
    }

    const url = new URL(modifiedString);

    let hostname = url.hostname === "0.0.0.0" ? "localhost" : url.hostname;

    const [hostnameWithoutPath] = hostname.split("/");
    const [hostnameWithoutQuery] = hostnameWithoutPath.split("?");
    hostname = hostnameWithoutQuery;

    if (url.port) {
      return `${hostname}:${url.port}`;
    }
    return hostname;
  } catch {
    return urlString.replace(/:$/, "");
  }
};

export const separateHostnameAndPort = (
  combinedString: string,
): { hostname: string; port: string } => {
  const [hostname, port] = combinedString.split(":");
  return { hostname, port: port ?? "" };
};

export const isLocalHost = (hostname: string) => {
  if (
    hostname.startsWith("localhost") ||
    /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/.test(hostname)
  ) {
    return true;
  }
  return false;
};

export const joinHostnameAndPort = (hostname: string, port: string): string =>
  `${hostname}:${port}`;

export const constructEndpointUrl = (
  value: string | null | undefined,
): string => {
  if (!value) return "";

  if (value.startsWith("http://") || value.startsWith("https://")) {
    return decodeURIComponent(value);
  }

  // Check if the endpoint is localhost or an IP address
  if (
    value.startsWith("localhost") ||
    /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/.test(value)
  ) {
    return `http://${decodeURIComponent(value)}`;
  }

  // For all other cases, default to HTTPS
  return `https://${decodeURIComponent(value)}`;
};

// workflows message labels

const formatLabelDate = (value: string) => {
  if (typeof value === "string" && value.match(/^\d{4}-\d{2}-\d{2}/)) {
    return formatDate(value, "natural");
  }
  return value;
};

const formatLabelValue = (value: string) => {
  const cleanValue = value.replace(/^"|"$/g, "").trim();

  if (cleanValue.startsWith("[") && cleanValue.endsWith("]")) {
    try {
      let arrayData: string[];
      try {
        arrayData = JSON.parse(cleanValue) as string[];
      } catch {
        const unescapedValue = cleanValue.replace(/\\"/g, '"');
        arrayData = JSON.parse(unescapedValue) as string[];
      }

      if (Array.isArray(arrayData)) {
        return arrayData.map((item) => formatLabelDate(item)).join(" to ");
      }
    } catch {
      return cleanValue;
    }
  }

  return formatLabelDate(cleanValue);
};

export const parseLabel = (label: string) =>
  label
    .split(/,\s*(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/)
    .map((item) => {
      if (!item.includes(":")) return null;

      const [keyPart, ...valueParts] = item.split(":");

      const value = valueParts.join(":");

      const key = keyPart.replace(/^"|"$/g, "").trim();
      const formattedValue = formatLabelValue(value.trim());

      return { key, value: formattedValue };
    })
    .filter(
      (item): item is { key: string; value: string } =>
        item?.key !== undefined && item.value !== undefined,
    );

export const encodeIfNeeded = (value: string) => {
  try {
    const decodedValue = decodeURIComponent(value);
    if (decodedValue === value) {
      return encodeURIComponent(value);
    }
    return value;
  } catch {
    return encodeURIComponent(value);
  }
};
