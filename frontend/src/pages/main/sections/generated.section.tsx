import { FCVM } from "@/utils/fcvm";
import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../main.vm";
import { useDroppable } from "@dnd-kit/core";
import { DraggableSticker } from "@/components/sticker/Sticker";
import { arrayMove, rectSortingStrategy, SortableContext } from "@dnd-kit/sortable";
import { twMerge } from "tailwind-merge";

export const GeneratedSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  const { setNodeRef, isOver } = useDroppable({
    id: "generated"
  });

  return (
    <div className={twMerge("h-full transition-colors rounded-lg", isOver && "bg-default-100")}>
      <div
        ref={setNodeRef}
        className={twMerge("flex flex-wrap gap-2 min-h-[180px] transition-colors")}>
        {vm.generatedStickers.map((item) => (
          <DraggableSticker key={item.id} item={item} />
        ))}
        {vm.generatedStickers.length === 0 && (
          <div className="flex flex-col items-center justify-center w-full h-full mt-8">
            <p className="text-default-500 text-sm">Создайте свой первый стикер в панели слева</p>
          </div>
        )}
      </div>
    </div>
  );
});
