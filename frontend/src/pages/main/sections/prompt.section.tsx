import { FCVM } from "@/utils/fcvm";
import { observer } from "mobx-react-lite";
import { MainPageViewModel, Prompt } from "../main.vm";
import { CardHeading } from "@/components/CardHeading";
import ChevronIcon from "@/assets/icons/chevron-down.svg";
import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Input,
  ScrollShadow,
  Textarea,
  Tooltip
} from "@nextui-org/react";
import PlusSvg from "@/assets/icons/plus.svg";
import MinusSvg from "@/assets/icons/minus.svg";
import DeleteSvg from "@/assets/icons/delete.svg";
import WandSvg from "@/assets/icons/wand.svg";
import { useState } from "react";
import { PromptCard } from "../components/prompt-card";
import { twMerge } from "tailwind-merge";

export const PromptSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
    <div className={twMerge("flex flex-col gap-2")}>
      {vm.selectedPattern && vm.stickerPatterns && (
        <Tooltip
          isDisabled={vm.isLoadingPattern}
          showArrow
          content="Нажмите для генерации по паттерну"
          placement="top-start">
          <ButtonGroup
            variant="solid"
            isDisabled={vm.isLoadingPattern}
            color="secondary"
            className={twMerge("justify-start w-fit", vm.prompts.length > 0 && "ml-6")}>
            <Button isLoading={vm.isLoadingPattern} onClick={() => vm.generateByPattern()}>
              {!vm.isLoadingPattern && <WandSvg className="w-5 h-5" />}
              {vm.selectedPattern?.description}
            </Button>
            <Dropdown placement="bottom-start">
              <DropdownTrigger>
                <Button isIconOnly>
                  <ChevronIcon className="w-4 h-4" />
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                disallowEmptySelection
                aria-label="Merge options"
                selectedKeys={[vm.selectedPattern?.title]}
                selectionMode="single"
                variant="shadow"
                className="max-w-[400px]">
                {Object.keys(vm.stickerPatterns).map((key) => (
                  <DropdownItem
                    key={key}
                    onClick={() => (vm.selectedPattern = vm.stickerPatterns![key])}>
                    {vm.stickerPatterns![key].description}
                  </DropdownItem>
                ))}
              </DropdownMenu>
            </Dropdown>
          </ButtonGroup>
        </Tooltip>
      )}
      <ScrollShadow className="flex flex-col gap-4 flex-1 overflow-auto bottom-inner-shadow pb-4">
        {vm.prompts.map((prompt, index) => (
          <div className="flex gap-2" key={index}>
            <span className="text-default-500 text-sm mt-1 w-4">{index + 1}.</span>
            <PromptCard
              prompt={prompt}
              onDelete={() => vm.removePrompt(index)}
              onGenerate={() => vm.generatePrompt(prompt)}
            />
          </div>
        ))}
        <div
          className={twMerge("sticky bottom-0 z-10 min-h-[40px]", vm.prompts.length > 0 && "ml-6")}>
          <Button
            startContent={<PlusSvg className="w-5 h-5" />}
            color="primary"
            size="sm"
            onClick={() => vm.addPrompt()}>
            Добавить промпт
          </Button>
        </div>
      </ScrollShadow>
    </div>
  );
});

export const PromptSectionHeader: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return <div className="flex items-center gap-1"></div>;
});
