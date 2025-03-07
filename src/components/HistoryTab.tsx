import { useEffect, useMemo, useState } from "react";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";

import { getPlaygroundSessionsAPI } from "@/api/playground";
import { HistoryEntry } from "@/types/playground";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useQueryState } from "nuqs";
import { HistoryItem } from "./HistoryItem";
import { HistoryBlankState } from "./HistoryBlankState";

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

export const HistoryTab = () => {
  const [agentId] = useQueryState("agent", {
    parse: (value) => value || undefined,
    history: "push",
  });
  const { selectedEndpoint } = usePlaygroundStore();
  const [sessions, setSessions] = useState<HistoryEntry[]>([]);

  useEffect(() => {
    if (selectedEndpoint && agentId) {
      getPlaygroundSessionsAPI(selectedEndpoint, agentId).then((response) => {
        setSessions(response);
      });
    }
  }, [selectedEndpoint, agentId]);

  const groupedHistory = useMemo(() => {
    const now = dayjs().utc();
    const yesterday = now.subtract(1, "day").startOf("day");

    return sessions.reduce((acc: GroupedHistory, entry) => {
      const entryDate = dayjs.unix(entry.created_at).utc();
      let group: string;

      if (entryDate.isAfter(yesterday)) {
        group = entryDate.isSame(now, "day") ? "Most recent" : "Yesterday";
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
  }, [sessions]);

  const handleLoadSession = (sessionId: string) => {
    // TODO: Implement session load functionality
    console.log("Load session", sessionId);
  };

  return (
    <div className="h-[calc(100vh-325px)] overflow-y-auto">
      {sessions.length === 0 ? (
        <HistoryBlankState />
      ) : (
        <div className="flex flex-col space-y-6 p-2 pb-6">
          {Object.entries(groupedHistory).map(([group, entries]) => (
            <div key={group} className="space-y-2">
              <h3 className="text-xs text-muted-foreground">{group}</h3>
              <div className="space-y-2">
                {entries.map((entry) => (
                  <HistoryItem
                    key={entry.session_id}
                    {...entry}
                    onLoadSession={handleLoadSession}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
