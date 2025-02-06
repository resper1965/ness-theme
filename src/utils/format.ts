import dayjs, { type Dayjs } from "dayjs";
import utc from "dayjs/plugin/utc"; // Import UTC plugin

// Register UTC plugin
dayjs.extend(utc);

export const formatDate = (
  date: string | Date | Dayjs | number,

  type:
    | "natural"
    | "natural-with-time"
    | "short"
    | "day"
    | "chart"
    | "time"
    | "natural-with-time-wo-meridiem"
    | "date-with-time"
    | "time-for-chat" = "natural",
) => {
  let format = "";

  if (type === "natural") {
    format = "MMM D, YYYY";
  } else if (type === "natural-with-time") {
    format = "MMM D, YYYY, h:mma";
  } else if (type === "date-with-time") {
    format = "MMM D, h:mm";
  } else if (type === "natural-with-time-wo-meridiem") {
    format = "MMM D, YYYY, h:mm";
  } else if (type === "short") {
    format = "M/D";
  } else if (type === "day") {
    format = "D";
  } else if (type === "chart") {
    format = "D MMM YYYY";
  } else if (type === "time") {
    format = "h:mma";
  } else if (type === "time-for-chat") {
    format = "h:mm:ss";
  }

  if (typeof date === "number") {
    return dayjs.unix(date).utc().format(format);
  }

  return dayjs(date).utc().format(format);
};

export const formatSeconds = (seconds: number) => `${seconds?.toFixed(2)} SEC`;
export const formatLargeNumber = (num: number): string => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1).replace(/\.0$/, "")}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1).replace(/\.0$/, "")}K`;
  }
  return num.toString();
};
