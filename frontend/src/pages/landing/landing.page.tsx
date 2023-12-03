import { observer } from "mobx-react-lite";
import { useState } from "react";
import { LandingPageViewModel } from "./landing.vm";
import { ControlledStickerCard } from "@/components/sticker/Sticker";
import cl from "./landing.module.scss";
import { twMerge } from "tailwind-merge";
import { FCVM } from "@/utils/fcvm";
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Divider,
  Spinner
} from "@nextui-org/react";
import ChevronSvg from "@/assets/icons/chevron-down.svg";
import WandSvg from "@/assets/icons/wand.svg";

export const Row = observer(({ vm, index }: { vm: LandingPageViewModel; index: number }) => {
  // get 6 pictures from vm.images and 4 images from vm.otherImages
  const imageAmount = 16;
  const images = vm.images.slice(index * imageAmount, index * imageAmount + imageAmount);
  const otherImagesKeys = Object.keys(vm.otherImages);
  const otherImagesKey = otherImagesKeys[index];
  if (!otherImagesKey) return null;
  const otherImages = vm.otherImages[otherImagesKey].slice(0, 8);
  const COLORS = ["linear-gradient(180deg, #0A2E36 0%, #003B4C 100%)", "#32174D", "#124F40"];
  // if imgSrc is empty retun null
  if (images.length === 0 || otherImages.length === 0) return null;
  if (!images[0].imgSrc || !otherImages[0].imgSrc)
    return (
      index === 0 && (
        <div className="flex justify-center items-center w-full h-full">
          <Spinner size={"lg"} color="primary" />
        </div>
      )
    );

  return (
    <div className={twMerge("flex w-full gap-6 mb-6", index % 2 === 0 && "flex-row-reverse")}>
      <div className="">
        <div className={twMerge(cl.grid6)}>
          {images.map((v) => (
            <div key={v.id} className="h-min">
              <ControlledStickerCard vm={v} onClick={() => vm.addSticker(v)} />
            </div>
          ))}
        </div>
      </div>
      <Card
        style={{
          background: COLORS[index % 3]
        }}>
        <CardBody>
          <div className={twMerge(cl.grid4)}>
            {otherImages.map((v) => (
              <div key={v.id} className="h-min">
                <ControlledStickerCard vm={v} onClick={() => vm.addSticker(v)} />
              </div>
            ))}
          </div>
        </CardBody>
      </Card>
    </div>
  );
});

export const LandingPage = observer(() => {
  const [vm] = useState(() => new LandingPageViewModel());

  return (
    <main className="flex w-full max-w-screen-xl mx-auto px-4 flex-col h-full overflow-y-scroll">
      <SelectedStickers vm={vm} />
      <div className="flex text-2xl mb-6 mt-4">StickyVerse</div>
      <div className="h-full overflow-y-auto pb-8">
        <Row vm={vm} index={0} />
        <Row vm={vm} index={1} />
        <Row vm={vm} index={2} />
      </div>
    </main>
  );
});

export const SelectedStickers: FCVM<LandingPageViewModel> = observer(({ vm }) => {
  const [hidden, setHidden] = useState(false);
  const filtered = vm.selectedStickers;

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
        <Button className="ml-auto" color="secondary" onClick={() => vm.navigateConstructor()}>
          <WandSvg className="w-5 h-5" />
          К редактору!
        </Button>
      </CardFooter>
    </Card>
  );
});
