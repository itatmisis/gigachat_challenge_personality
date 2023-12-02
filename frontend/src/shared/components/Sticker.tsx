import { useDraggable } from "@dnd-kit/core";
import { useSortable } from "@dnd-kit/sortable";
import { StickerDto } from "api/models/sticker.model";
import { CSS } from "@dnd-kit/utilities";
import { twMerge } from "tailwind-merge";

export const DraggableSticker = ({ item }: { item: StickerDto }) => {
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
      <Sticker item={item} />
    </div>
  );
};

export const Sticker = ({ item }: { item: StickerDto }) => {
  return (
    <div className="flex flex-col items-center justify-center w-32 h-32 rounded-lg bg-white shadow-lg">
      {item.id}
    </div>
  );
};
