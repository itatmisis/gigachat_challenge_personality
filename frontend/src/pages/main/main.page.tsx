import React, { FC, PropsWithChildren, ReactNode, useState } from "react";
import { GeneratedSection } from "./sections/generated.section";
import { observer } from "mobx-react-lite";
import { FavoritesSection } from "./sections/favorites.section";
import { PromptSection, PromptSectionHeader } from "./sections/prompt.section";
import { MainPageViewModel } from "./main.vm";
import cl from "./style.module.scss";
import { Card, CardBody, CardHeader, Divider } from "@nextui-org/react";
import { twMerge } from "tailwind-merge";
import { CardHeading } from "@/components/CardHeading";

export const Section = ({
  children,
  className,
  heading,
  actions
}: {
  children?: ReactNode;
  className?: string;
  heading?: string;
  actions?: ReactNode;
}) => {
  return (
    <Card className={twMerge("bg-default-50 rounded-lg shadow-lg h-full", className)}>
      {heading && (
        <>
          <CardHeader className="flex justify-between items-center">
            <CardHeading>{heading}</CardHeading>
            {actions}
          </CardHeader>
          <Divider />
        </>
      )}
      <CardBody className="h-full">{children}</CardBody>
    </Card>
  );
};

export const MainPage = observer(() => {
  const [vm] = useState(() => new MainPageViewModel());

  return (
    <main className={twMerge(cl.layout, "px-4 my-24 gap-4 h-full overflow-hidden")}>
      <Section
        className="[grid-area:prompt]"
        heading="Генерация"
        actions={<PromptSectionHeader vm={vm} />}>
        <PromptSection vm={vm} />
        <Card />
      </Section>
      <Section className="[grid-area:generated]">
        <GeneratedSection vm={vm} />
      </Section>
      <Section className="[grid-area:favorites]">
        <FavoritesSection vm={vm} />
      </Section>
    </main>
  );
});
