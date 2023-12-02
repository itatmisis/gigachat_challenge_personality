import { FCVM } from "@/utils/fcvm";
import { observer } from "mobx-react-lite";
import { MainPageViewModel } from "../main.vm";
import { useDroppable } from "@dnd-kit/core";
import { DraggableSticker } from "@/components/Sticker";
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
      </div>
    </div>
  );
});
