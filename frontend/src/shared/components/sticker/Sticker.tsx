import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { twMerge } from "tailwind-merge";
import { Checkbox, Skeleton } from "@nextui-org/react";
import { Sticker } from "../../../pages/main/main.vm";
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

export const StickerCard = observer(({ item }: { item: Sticker }) => {
  return (
    <Skeleton isLoaded={!item.isLoading} className="rounded-lg">
      <div
        className="flex flex-col items-center justify-center w-32 h-32"
        onClick={(e) => {
          console.log("god it");
        }}>
        {item.img && <img src={`data:image/png;base64,${item.img}`} alt={item.prompt} />}
      </div>
    </Skeleton>
  );
});

export const ControlledStickerCard = observer((x: { item: Sticker }) => {
  return (
    <Skeleton isLoaded={!x.item.isLoading} className="rounded-lg">
      <div className="flex flex-col items-center justify-center w-32 h-32 relative">
        {x.item.img && <img src={`data:image/png;base64,${x.item.img}`} alt={x.item.prompt} />}
        <Checkbox
          className="absolute top-2 left-2"
          checked={x.item.isSelected}
          onChange={(v) => (x.item.isSelected = v.target.checked)}
        />
      </div>
    </Skeleton>
  );
});
