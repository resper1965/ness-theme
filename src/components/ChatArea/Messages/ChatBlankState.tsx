"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import Icon from "@/components/ui/icon";
import { IconType } from "@/components/ui/icon/types";

const AgnoTag = () => {
  return (
    <svg
      width="101"
      height="56"
      viewBox="0 0 101 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g filter="url(#filter0_dd_2859_5300)">
        <rect
          x="11.6504"
          y="6.56763"
          width="76"
          height="28"
          rx="8"
          transform="rotate(-3.82708 11.6504 6.56763)"
          fill="#FAFAFA"
          shapeRendering="geometricPrecision"
        />
        <g clipPath="url(#clip0_2859_5300)">
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M35.7024 11.2754C36.1945 12.1001 36.2693 13.2177 36.4188 15.4529L36.8994 22.6374C37.0489 24.8726 37.1237 25.9902 36.7458 26.8731C36.4134 27.6496 35.8437 28.301 35.1183 28.7339C34.2937 29.226 33.1761 29.3008 30.9408 29.4503L23.7563 29.9309C21.5211 30.0804 20.4035 30.1552 19.5207 29.7773C18.7441 29.4449 18.0927 28.8752 17.6598 28.1498C17.1677 27.3252 17.0929 26.2076 16.9434 23.9724L16.4628 16.7878C16.3133 14.5526 16.2385 13.435 16.6164 12.5522C16.9488 11.7756 17.5185 11.1242 18.2439 10.6913C19.0686 10.1992 20.1862 10.1245 22.4214 9.97493L29.6059 9.49432C31.8411 9.3448 32.9587 9.27004 33.8416 9.64793C34.6181 9.98033 35.2695 10.55 35.7024 11.2754ZM22.802 14.5601L27.829 14.2239L32.6254 24.3203L30.5336 24.4602L26.7197 16.0701L22.92 16.3243L22.802 14.5601ZM20.5341 23.3571L25.6815 23.0127L25.7995 24.7769L20.6521 25.1212L20.5341 23.3571Z"
            fill="#FF4017"
          />
        </g>
        <path
          d="M47.0613 24.2435L45.5873 24.3421L49.0739 12.4465L50.5252 12.3495L55.565 23.6747L54.0911 23.7733L49.9677 14.2318L49.877 14.2378L47.0613 24.2435ZM47.3022 19.6718L53.2434 19.2744L53.3269 20.5216L47.3856 20.919L47.3022 19.6718ZM60.9375 26.7776C60.2912 26.8208 59.7301 26.7748 59.2541 26.6396C58.7784 26.5082 58.3766 26.3187 58.0487 26.0711C57.7249 25.827 57.4621 25.5598 57.2605 25.2696L58.2762 24.45C58.4078 24.6006 58.573 24.7718 58.7718 24.9635C58.9709 25.159 59.2362 25.3216 59.5675 25.4513C59.9029 25.5845 60.3333 25.6335 60.8586 25.5984C61.5616 25.5514 62.1304 25.3425 62.5649 24.9717C62.9995 24.601 63.1925 24.0528 63.144 23.3271L63.0256 21.5584L62.9123 21.566C62.8246 21.7313 62.6979 21.9371 62.5322 22.1836C62.37 22.426 62.1267 22.6492 61.8025 22.8531C61.4818 23.053 61.038 23.1719 60.4711 23.2098C59.7681 23.2569 59.1258 23.1328 58.5442 22.8376C57.9664 22.5422 57.4937 22.0879 57.1262 21.4747C56.7625 20.8612 56.5503 20.101 56.4896 19.1939C56.4299 18.3019 56.5348 17.5148 56.8043 16.8324C57.0735 16.1462 57.4756 15.603 58.0107 15.2028C58.5455 14.7988 59.1796 14.5722 59.9128 14.5232C60.4797 14.4853 60.9358 14.5497 61.281 14.7164C61.6297 14.8791 61.9009 15.0735 62.0945 15.2997C62.2916 15.5219 62.4443 15.7053 62.5527 15.8499L62.6887 15.8408L62.5962 14.4576L63.8888 14.3711L64.4879 23.3283C64.538 24.0767 64.4086 24.6965 64.0998 25.1879C63.7951 25.6829 63.3647 26.059 62.8086 26.3164C62.2566 26.5773 61.6329 26.731 60.9375 26.7776ZM60.5721 21.9958C61.1088 21.9599 61.5541 21.8068 61.908 21.5363C62.262 21.2659 62.5199 20.8937 62.6818 20.4197C62.8437 19.9457 62.9032 19.3875 62.8602 18.745C62.8182 18.1176 62.6867 17.5702 62.4656 17.1029C62.2446 16.6355 61.9397 16.2782 61.5511 16.0308C61.1626 15.7835 60.6961 15.678 60.1519 15.7144C59.585 15.7523 59.1222 15.9276 58.7634 16.2401C58.4085 16.5523 58.1527 16.9567 57.9961 17.4531C57.8433 17.9492 57.7866 18.4921 57.826 19.0817C57.8665 19.6864 57.9967 20.2149 58.2168 20.6671C58.4404 21.1153 58.7481 21.4592 59.14 21.6987C59.5354 21.9342 60.0127 22.0332 60.5721 21.9958ZM67.9078 17.5873L68.2583 22.8256L66.9203 22.9151L66.3378 14.2073L67.6304 14.1208L67.7214 15.4814L67.8348 15.4738C68.0093 15.018 68.2954 14.642 68.6932 14.3458C69.0908 14.0459 69.6183 13.8739 70.276 13.8299C70.8656 13.7905 71.3895 13.8769 71.8479 14.0892C72.306 14.2978 72.6742 14.6376 72.9525 15.1087C73.2305 15.576 73.3943 16.1801 73.4439 16.9208L73.814 22.4539L72.4761 22.5434L72.112 17.101C72.0663 16.417 71.853 15.8959 71.4722 15.538C71.0911 15.1763 70.5907 15.0161 69.9709 15.0576C69.5438 15.0861 69.1683 15.2043 68.8443 15.412C68.5241 15.6194 68.2795 15.9072 68.1105 16.2754C67.9415 16.6435 67.874 17.0808 67.9078 17.5873ZM79.8085 22.2351C79.0224 22.2877 78.3201 22.1468 77.7017 21.8123C77.0871 21.4776 76.591 20.985 76.2134 20.3345C75.8396 19.6838 75.6226 18.9086 75.5624 18.0091C75.5018 17.1021 75.6132 16.2993 75.8968 15.6008C76.1841 14.902 76.61 14.3458 77.1746 13.9322C77.7429 13.5184 78.4202 13.2851 79.2063 13.2325C79.9924 13.18 80.6928 13.321 81.3074 13.6557C81.9258 13.9902 82.422 14.4847 82.7961 15.1392C83.174 15.7935 83.3932 16.5742 83.4539 17.4812C83.5141 18.3807 83.4004 19.178 83.1128 19.873C82.829 20.5677 82.4029 21.122 81.8345 21.5359C81.27 21.9495 80.5946 22.1826 79.8085 22.2351ZM79.7281 21.0333C80.3253 20.9933 80.8064 20.8074 81.1714 20.4755C81.5364 20.1436 81.7948 19.722 81.9466 19.2107C82.0985 18.6994 82.1549 18.1528 82.116 17.5707C82.077 16.9887 81.9482 16.4525 81.7293 15.9623C81.5105 15.472 81.198 15.0848 80.7918 14.8007C80.3855 14.5165 79.8838 14.3945 79.2867 14.4344C78.6895 14.4743 78.2086 14.6622 77.8438 14.9979C77.479 15.3336 77.2209 15.759 77.0693 16.274C76.9177 16.7891 76.8614 17.3376 76.9004 17.9196C76.9393 18.5017 77.068 19.0359 77.2866 19.5224C77.5052 20.0089 77.8174 20.3923 78.2234 20.6727C78.6294 20.953 79.131 21.0732 79.7281 21.0333Z"
          fill="#18181B"
        />
      </g>
      <defs>
        <filter
          id="filter0_dd_2859_5300"
          x="-0.349609"
          y="-0.505127"
          width="101.699"
          height="57.0103"
          filterUnits="userSpaceOnUse"
          colorInterpolationFilters="sRGB"
        >
          <feFlood floodOpacity="0" result="BackgroundImageFix" />
          <feColorMatrix
            in="SourceAlpha"
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
            result="hardAlpha"
          />
          <feMorphology
            radius="2"
            operator="erode"
            in="SourceAlpha"
            result="effect1_dropShadow_2859_5300"
          />
          <feOffset dy="8" />
          <feGaussianBlur stdDeviation="6" />
          <feComposite in2="hardAlpha" operator="out" />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.08 0"
          />
          <feBlend
            mode="normal"
            in2="BackgroundImageFix"
            result="effect1_dropShadow_2859_5300"
          />
          <feColorMatrix
            in="SourceAlpha"
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
            result="hardAlpha"
          />
          <feMorphology
            radius="3"
            operator="erode"
            in="SourceAlpha"
            result="effect2_dropShadow_2859_5300"
          />
          <feOffset dy="3" />
          <feGaussianBlur stdDeviation="2.5" />
          <feComposite in2="hardAlpha" operator="out" />
          <feColorMatrix
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.08 0"
          />
          <feBlend
            mode="normal"
            in2="effect1_dropShadow_2859_5300"
            result="effect2_dropShadow_2859_5300"
          />
          <feBlend
            mode="normal"
            in="SourceGraphic"
            in2="effect2_dropShadow_2859_5300"
            result="shape"
          />
        </filter>
        <clipPath id="clip0_2859_5300">
          <rect
            width="20"
            height="20"
            fill="white"
            transform="translate(15.9087 10.2917) rotate(-3.82708)"
          />
        </clipPath>
      </defs>
    </svg>
  );
};

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
              <AgnoTag />
            </span>
            <span className="flex items-center font-[600]">
              Agent UI, built with
            </span>
            <span className="inline-flex items-center translate-y-[10px] scale-125">
              <div className="relative w-[90px] h-[40px]">
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
