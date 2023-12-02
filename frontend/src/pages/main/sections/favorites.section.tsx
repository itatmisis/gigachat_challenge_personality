import { FCVM } from "@/utils/fcvm";
import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../main.vm";
import { useDroppable } from "@dnd-kit/core";
import { DraggableSticker } from "@/components/sticker/Sticker";
import { arrayMove, rectSortingStrategy, SortableContext } from "@dnd-kit/sortable";
import { twMerge } from "tailwind-merge";
import { Button } from "@nextui-org/react";

export const FavoritesSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const { setNodeRef, isOver } = useDroppable({
    id: "favorite"
  });

  return (
    <div className={twMerge("h-full transition-colors rounded-lg", isOver && "bg-default-100")}>
      <div ref={setNodeRef} className={twMerge("flex flex-wrap gap-2 min-h-[180px]")}>
        {vm.favoriteStickers.map((item) => (
          <DraggableSticker key={item.id} item={item} />
        ))}
        {vm.favoriteStickers.length === 0 && (
          <div className="flex flex-col items-center justify-center w-full h-full mt-8">
            <p className="text-default-500 text-sm">
              Перетащите сюда готовые стикеры для создания стикерпака
            </p>
          </div>
        )}
      </div>
    </div>
  );
});

export const FavoritesFooter: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
    <div className="flex items-center gap-1 ml-auto">
      <Button size="sm" color="primary" isDisabled={vm.favoriteStickers.length === 0}>
        Опубликовать
      </Button>
    </div>
  );
});
