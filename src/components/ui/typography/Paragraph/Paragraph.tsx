import { type FC } from "react";

import { cn } from "@/utils/cn";

import { PARAGRAPH_SIZES } from "./constants";
import { type ParagraphProps } from "./types";

const Paragraph: FC<ParagraphProps> = ({
  children,
  size = "default",
  className,
  id,
}) => (
  <p id={id} className={cn(PARAGRAPH_SIZES[size], className)}>
    {children}
  </p>
);

export default Paragraph;
