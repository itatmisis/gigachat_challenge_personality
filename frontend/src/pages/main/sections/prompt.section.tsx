import { FCVM } from "@/utils/fcvm";
import { observer } from "mobx-react-lite";
import { MainPageViewModel, Prompt } from "../main.vm";
import { CardHeading } from "@/components/CardHeading";
import { Button, Card, CardBody, Divider, Input, ScrollShadow, Textarea } from "@nextui-org/react";
import PlusSvg from "@/assets/icons/plus.svg";
import MinusSvg from "@/assets/icons/minus.svg";
import DeleteSvg from "@/assets/icons/delete.svg";
import WandSvg from "@/assets/icons/wand.svg";
import { useState } from "react";
import { PromptCard } from "../components/prompt-card";

export const PromptSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
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
      <div className="sticky bottom-0 z-10 min-h-[40px] ml-6">
        <Button
          startContent={<PlusSvg className="w-5 h-5" />}
          color="primary"
          size="sm"
          onClick={() => vm.addPrompt()}>
          Добавить промпт
        </Button>
      </div>
    </ScrollShadow>
  );
});

export const PromptSectionHeader: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return <div className="flex items-center gap-1"></div>;
});
