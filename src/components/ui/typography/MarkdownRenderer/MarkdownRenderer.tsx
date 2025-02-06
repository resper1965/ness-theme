import { type FC } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

import { cn } from "@/utils/cn";

import { type MarkdownRendererProps } from "./types";

const MarkdownRenderer: FC<MarkdownRendererProps> = ({
  children,
  classname,
}) => (
  <ReactMarkdown
    className={cn(
      "prose prose-h1:text-xl dark:prose-invert flex w-full flex-col gap-y-5 rounded-lg",
      classname,
    )}
    remarkPlugins={[remarkGfm]}
    rehypePlugins={[rehypeRaw, rehypeSanitize]}
  >
    {children}
  </ReactMarkdown>
);

export default MarkdownRenderer;
