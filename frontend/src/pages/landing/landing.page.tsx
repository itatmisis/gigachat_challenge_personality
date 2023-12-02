import { observer } from "mobx-react-lite";
import { useState } from "react";
import { LandingPageViewModel } from "./landing.vm";
import { ControlledStickerCard } from "@/components/sticker/Sticker";
import cl from "./landing.module.scss";
import { twMerge } from "tailwind-merge";
import { FCVM } from "@/utils/fcvm";
import { Button, Card, CardBody, CardFooter, CardHeader, Divider } from "@nextui-org/react";
import ChevronSvg from "@/assets/icons/chevron-down.svg";
import WandSvg from "@/assets/icons/wand.svg";

export const LandingPage = observer(() => {
  const [vm] = useState(() => new LandingPageViewModel());

  return (
    <main className="flex w-full max-w-screen-desktop mx-auto px-4 flex-col h-full overflow-y-scroll relative">
      <SelectedStickers vm={vm} />
      <div className="flex">Вдохновение</div>
      <div className="h-full overflow-y-auto">
        <div className={twMerge(cl.grid)}>
          {vm.images.map((v) => (
            <div key={v.id} className="h-min">
              <ControlledStickerCard vm={v} />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
});

export const SelectedStickers: FCVM<LandingPageViewModel> = observer(({ vm }) => {
  const [hidden, setHidden] = useState(false);
  const filtered = vm.images.filter((v) => v.isSelected);

  return (
    <Card
      className={twMerge(
        "absolute bottom-4 right-4 w-[300px] z-10 max-h-[600px]",
        hidden && "max-h-[48px] overflow-hidden"
      )}>
      <CardHeader
        className="h-12 hover:bg-default-100 cursor-pointer justify-between"
        onClick={() => setHidden((v) => !v)}>
        Выбранные стикеры: {vm.images.filter((v) => v.isSelected).length}
        <ChevronSvg
          className={twMerge("w-4 h-4 transform transition-transform", hidden && "rotate-180")}
        />
      </CardHeader>
      <Divider />
      <CardBody className="gap-2">
        <div className={cl.gridSmall}>
          {filtered.map((v) => (
            <ControlledStickerCard vm={v} readonly key={v.id} />
          ))}
        </div>
        {filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center w-full h-full">
            <p className="text-default-500 text-sm">Выберите стикеры</p>
          </div>
        )}
      </CardBody>
      <Divider />
      <CardFooter>
        <Button className="ml-auto" color="secondary">
          <WandSvg className="w-5 h-5" />
          Начать слияние
        </Button>
      </CardFooter>
    </Card>
  );
});
