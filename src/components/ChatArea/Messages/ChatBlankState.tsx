"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import Icon from "@/components/ui/icon";
import { IconType } from "@/components/ui/icon/types";

const EXTERNAL_LINKS = {
  documentation:
    "https://docs.agno.com/get-started/playground#agent-playground",
  playground: "https://app.agno.com/playground/chat",
};

const TECH_ICONS = [
  {
    type: "nextjs" as IconType,
    position: "left-0 top-0 z-10",
    link: "https://nextjs.org",
    name: "Next.js",
  },
  {
    type: "shadcn" as IconType,
    position: "left-[15px] top-0 z-20",
    link: "https://ui.shadcn.com",
    name: "shadcn/ui",
  },
  {
    type: "tailwind" as IconType,
    position: "left-[30px] top-0 z-30",
    link: "https://tailwindcss.com",
    name: "Tailwind CSS",
  },
];

interface ActionButtonProps {
  href: string;
  variant?: "primary";
  text: string;
}

const ActionButton = ({ href, variant, text }: ActionButtonProps) => {
  const baseStyles =
    "px-4 py-2 text-sm transition-colors font-dmmono tracking-tight";
  const variantStyles = {
    primary: "border border-border hover:bg-neutral-800 rounded-xl",
  };

  return (
    <Link
      href={href}
      target="_blank"
      className={`${baseStyles} ${variant ? variantStyles[variant] : ""}`}
    >
      {text}
    </Link>
  );
};

export const ChatBlankState = () => {
  return (
    <section
      className="flex flex-col items-center text-center font-geist"
      aria-label="Welcome message"
    >
      <div className="max-w-3xl flex flex-col gap-y-8">
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="text-3xl font-[600] tracking-tight"
        >
          <div className="flex items-center justify-center whitespace-nowrap gap-x-2 font-medium">
            <span className="flex items-center font-[600]">
              This is an open-source
            </span>
            <span className="inline-flex items-center translate-y-[10px] scale-125">
              <Icon type="agnoTag" size="default" />
            </span>
            <span className="flex items-center font-[600]">
              Agent UI, built with
            </span>
            <span className="inline-flex items-center translate-y-[5px] scale-125">
              <div className="relative w-[90px] h-[40px] ml-2">
                {TECH_ICONS.map((icon) => (
                  <div
                    key={icon.type}
                    className={`absolute ${icon.position} group`}
                  >
                    <Link
                      href={icon.link}
                      target="_blank"
                      rel="noopener"
                      className="block cursor-pointer"
                    >
                      <div className="transform transition-transform duration-200 group-hover:-translate-y-2">
                        <Icon type={icon.type} size="default" />
                      </div>
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-1 bg-transparent text-primary text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
                        {icon.name}
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            </span>
          </div>
          <p>You can learn more on the Agent Playground.</p>
        </motion.h1>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="flex gap-4 justify-center"
        >
          <ActionButton
            href={EXTERNAL_LINKS.documentation}
            variant="primary"
            text="GO TO OUR DOCS"
          />
          <ActionButton
            href={EXTERNAL_LINKS.playground}
            text="VISIT AGENT PLAYGROUND"
          />
        </motion.div>
      </div>
    </section>
  );
};
