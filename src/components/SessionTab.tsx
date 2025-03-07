import { useEffect, useMemo, useState } from "react";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";

import { getAllPlaygroundSessionsAPI } from "@/api/playground";
import { HistoryEntry } from "@/types/playground";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useQueryState } from "nuqs";
import { SessionItem } from "./SessionItem";
import SessionBlankState from "./SessionBlankState";

dayjs.extend(utc);

interface GroupedHistory {
  [key: string]: HistoryEntry[];
}

const formatDate = (
  timestamp: number,
  format: "natural" | "full" = "full",
): string => {
  const date = dayjs.unix(timestamp).utc();
  return format === "natural"
    ? date.format("HH:mm")
    : date.format("YYYY-MM-DD HH:mm:ss");
};

export const SessionTab = () => {
  const [agentId] = useQueryState("agent", {
    parse: (value) => value || undefined,
    history: "push",
  });
  const { selectedEndpoint } = usePlaygroundStore();
  const { historyData, setHistoryData } = usePlaygroundStore();
  const [isScrolling, setIsScrolling] = useState(false);

  const handleScroll = () => {
    setIsScrolling(true);
    let scrollTimer = setTimeout(() => {
      setIsScrolling(false);
    }, 1000);
  };

  useEffect(() => {
    if (selectedEndpoint && agentId) {
      getAllPlaygroundSessionsAPI(selectedEndpoint, agentId).then(
        (response) => {
          setHistoryData(response);
        },
      );
    }
  }, [selectedEndpoint, agentId, setHistoryData]);

  const groupedHistory = useMemo(() => {
    const now = dayjs().utc();
    const yesterday = now.subtract(1, "day").startOf("day");

    return historyData.reduce((acc: GroupedHistory, entry) => {
      const entryDate = dayjs.unix(entry.created_at).utc();
      let group: string;

      if (entryDate.isAfter(yesterday)) {
        group = entryDate.isSame(now, "day") ? "Most Recent" : "Yesterday";
      } else {
        group = "Older";
      }

      if (!acc[group]) {
        acc[group] = [];
      }
      const formattedEntry = {
        ...entry,
        created_at: entry.created_at,
        formatted_time: formatDate(entry.created_at, "natural"),
      };
      acc[group].push(formattedEntry);
      return acc;
    }, {});
  }, [historyData]);

  return (
    <div>
      <div className="text-xs font-medium uppercase mb-2">Sessions</div>
      <div
        className={`h-[calc(100vh-325px)] overflow-y-auto transition-all duration-300 font-geist [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar]:transition-opacity [&::-webkit-scrollbar]:duration-300
        ${isScrolling ? "[&::-webkit-scrollbar]:opacity-0 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-background" : "[&::-webkit-scrollbar]:opacity-100"}`}
        onScroll={handleScroll}
        onMouseEnter={() => setIsScrolling(true)}
        onMouseLeave={() => {
          setTimeout(() => setIsScrolling(false), 2000);
        }}
      >
        {historyData.length === 0 ? (
          <SessionBlankState />
        ) : (
          <div className="flex flex-col space-y-6 p-2 pb-6">
            {Object.entries(groupedHistory).map(([group, entries]) => (
              <div key={group} className="space-y-2">
                <h3 className="text-xs text-muted-foreground">{group}</h3>
                <div className="space-y-2">
                  {entries.map((entry) => (
                    <SessionItem key={entry.session_id} {...entry} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
