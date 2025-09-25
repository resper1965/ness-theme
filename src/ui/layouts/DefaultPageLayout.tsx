"use client";
/*
 * Documentation:
 * Default Page Layout — https://app.subframe.com/a1f5e87aed2f/library?component=Default+Page+Layout_a57b1c43-310a-493f-b807-8cc88e2452cf
 * Sidebar rail with icons — https://app.subframe.com/a1f5e87aed2f/library?component=Sidebar+rail+with+icons_0d7efe0e-8762-46f5-b399-9f6d329e13b9
 */

import React from "react";
import { FeatherBell } from "@subframe/core";
import { FeatherBot } from "@subframe/core";
import { FeatherHistory } from "@subframe/core";
import { FeatherHome } from "@subframe/core";
import { FeatherSettings } from "@subframe/core";
import { SidebarRailWithIcons } from "../components/SidebarRailWithIcons";
import * as SubframeUtils from "../utils";

interface DefaultPageLayoutRootProps
  extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
  className?: string;
}

const DefaultPageLayoutRoot = React.forwardRef<
  HTMLDivElement,
  DefaultPageLayoutRootProps
>(function DefaultPageLayoutRoot(
  { children, className, ...otherProps }: DefaultPageLayoutRootProps,
  ref
) {
  return (
    <div
      className={SubframeUtils.twClassNames(
        "flex h-screen w-full items-start",
        className
      )}
      ref={ref}
      {...otherProps}
    >
      <SidebarRailWithIcons
        header={
          <div className="flex flex-col flex-wrap items-center justify-between px-1 py-1">
            <img className="h-6 w-6 flex-none object-cover [clip-path:circle()]" />
          </div>
        }
        footer={
          <>
            <SidebarRailWithIcons.NavItem icon={<FeatherBell />}>
              Item
            </SidebarRailWithIcons.NavItem>
            <SidebarRailWithIcons.NavItem icon={<FeatherSettings />}>
              Item
            </SidebarRailWithIcons.NavItem>
          </>
        }
      >
        <SidebarRailWithIcons.NavItem icon={<FeatherHome />} selected={true}>
          Home
        </SidebarRailWithIcons.NavItem>
        <SidebarRailWithIcons.NavItem icon={<FeatherBot />}>
          Gabi.OS
        </SidebarRailWithIcons.NavItem>
        <SidebarRailWithIcons.NavItem icon={<FeatherHistory />}>
          Historico
        </SidebarRailWithIcons.NavItem>
      </SidebarRailWithIcons>
      {children ? (
        <div className="flex grow shrink-0 basis-0 flex-col items-start gap-2 self-stretch overflow-y-auto bg-default-background">
          {children}
        </div>
      ) : null}
    </div>
  );
});

export const DefaultPageLayout = DefaultPageLayoutRoot;
