import { useDraggable } from "@dnd-kit/core";
import { useSortable } from "@dnd-kit/sortable";
import { StickerDto } from "api/models/sticker.model";
import { CSS } from "@dnd-kit/utilities";
import { twMerge } from "tailwind-merge";
import { Skeleton } from "@nextui-org/react";
import { Sticker } from "../../pages/main/main.vm";
import { observer } from "mobx-react-lite";

export const DraggableSticker = observer(({ item }: { item: Sticker }) => {
  const { attributes, isDragging, listeners, setNodeRef, transform, transition } = useSortable({
    id: item.id
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={twMerge(isDragging && "brightness-110 z-50")}>
      <StickerCard item={item} />
    </div>
  );
});
// f477575c-4a66-44f4-a6f6-99b305d50d48
export const StickerCard = observer(({ item }: { item: Sticker }) => {
  return (
    <Skeleton isLoaded={!item.isLoading} className="rounded-lg">
      <div className="flex flex-col items-center justify-center w-32 h-32">
        {item.img && <img src={`data:image/png;base64,${item.img}`} alt={item.prompt} />}
      </div>
    </Skeleton>
  );
});
