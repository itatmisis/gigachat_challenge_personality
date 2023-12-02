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
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  closestCorners
} from "@dnd-kit/core";
import { SortableContext, rectSortingStrategy } from "@dnd-kit/sortable";
import { Sticker } from "@/components/Sticker";

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
          <CardHeader className="flex justify-between items-center h-[56px]">
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
  const [draggedItem, setDraggedItem] = useState<string | null>(null);

  const handleDragEnd = (event: DragEndEvent) => {
    setDraggedItem(null);
    const { active, over } = event;

    if (over?.id === "favorite") {
      vm.moveToFavorites(active.id.toString());
      return;
    }
    if (over?.id === "generated") {
      vm.moveToGenerated(active.id.toString());
      return;
    }
    if (over && active.id !== over.id) {
      vm.moveSticker(over.id.toString(), active.id.toString());
    }
  };

  const handleDragStart = (event: DragStartEvent) => {
    setDraggedItem(event.active.id.toString());
  };

  return (
    <DndContext onDragEnd={handleDragEnd} onDragStart={handleDragStart}>
      <DragOverlay>
        {draggedItem && (
          <Sticker item={vm.stickers.find((item) => item.id.toString() === draggedItem)!} />
        )}
      </DragOverlay>
      <SortableContext items={vm.stickers} strategy={rectSortingStrategy}>
        <main className={twMerge(cl.layout, "px-4 my-12 gap-4 h-full overflow-hidden")}>
          <Section
            className="[grid-area:prompt]"
            heading="Генерация"
            actions={<PromptSectionHeader vm={vm} />}>
            <PromptSection vm={vm} />
            <Card />
          </Section>

          <Section className="[grid-area:generated]" heading="Результат">
            <GeneratedSection vm={vm} />
          </Section>
          <Section className="[grid-area:favorites]" heading="">
            <FavoritesSection vm={vm} />
          </Section>
        </main>
      </SortableContext>
    </DndContext>
  );
});
