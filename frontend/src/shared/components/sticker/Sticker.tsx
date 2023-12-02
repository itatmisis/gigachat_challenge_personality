import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { twMerge } from "tailwind-merge";
import { Skeleton } from "@nextui-org/react";
import { Sticker } from "../../../pages/main/main.vm";
import { observer } from "mobx-react-lite";
import CheckSvg from "@/assets/icons/check.svg";
import { StickerViewModel } from "./sticker.vm";
import { useEffect } from "react";

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

export const ControlledStickerCard = observer(
  ({
    vm,
    readonly,
    onClick
  }: {
    vm: StickerViewModel;
    readonly?: boolean;
    onClick?: () => void;
  }) => {
    return (
      <Skeleton
        isLoaded={!vm.isLoading}
        className={twMerge(
          "appear rounded-lg aspect-square transition-all",
          !readonly && "cursor-pointer",
          vm.isSelected && "scale-95"
        )}>
        <div className="flex flex-col items-center justify-center relative">
          {vm.img ||
            (vm.imgSrc && (
              <img
                src={vm.img ? `data:image/png;base64,${vm.img}` : vm.imgSrc ?? undefined}
                alt=""
                onClick={() => {
                  if (readonly) return;
                  if (onClick) {
                    onClick();
                  } else {
                    vm.isSelected = !vm.isSelected;
                  }
                }}
              />
            ))}
          {!readonly && <CheckMark checked={vm.isSelected} />}
        </div>
      </Skeleton>
    );
  }
);

const CheckMark = ({ checked }: { checked: boolean }) => {
  return (
    <div
      className={twMerge(
        "absolute top-2 left-2 w-4 h-4 rounded-md flex items-center justify-center bg-black",
        checked && "bg-primary"
      )}>
      {checked && <CheckSvg className="text-white w-3 h-3 pointer-events-none" />}
    </div>
  );
};
