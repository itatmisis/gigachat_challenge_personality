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

const PromptCard = observer(
  ({ prompt, onDelete, disabled }: { prompt: Prompt; onDelete: () => void; disabled: boolean }) => {
    return (
      <div className="flex gap-2">
        <Card className="bg-default-100 flex-1" shadow="none">
          <CardBody>
            <div className="flex gap-2">
              <div className="flex flex-col gap-2 flex-1">
                <Textarea
                  isDisabled={disabled}
                  label="Промпт"
                  variant="faded"
                  value={prompt.positive}
                  onChange={(e) => (prompt.positive = e.target.value)}
                />
                <Input
                  isDisabled={disabled}
                  label="Негативный промпт"
                  variant="flat"
                  size="sm"
                  value={prompt.negative}
                  onChange={(e) => (prompt.negative = e.target.value)}
                />
              </div>
              <div className="flex flex-col">
                <span className="text-default-500 text-sm">Количество</span>
                <div className="flex items-center">
                  <Button
                    isDisabled={disabled}
                    onClick={() => (prompt.count = Math.max(prompt.count - 1, 0))}
                    isIconOnly
                    color="primary"
                    size="sm"
                    variant="light">
                    <MinusSvg className="w-5 h-5" />
                  </Button>
                  <span className="text-default-500 w-6 text-center">{prompt.count}</span>
                  <Button
                    isDisabled={disabled}
                    onClick={() => (prompt.count = Math.min(prompt.count + 1, 100))}
                    isIconOnly
                    color="primary"
                    size="sm"
                    variant="light">
                    <PlusSvg className="w-5 h-5" />
                  </Button>
                </div>
              </div>
            </div>
            {/* <div className="flex items-center mt-3 mx-2"></div> */}
          </CardBody>
        </Card>
        <Button
          isDisabled={disabled}
          onClick={() => onDelete()}
          isIconOnly
          color="danger"
          size="sm"
          variant="light">
          <DeleteSvg className="w-5 h-5" />
        </Button>
      </div>
    );
  }
);

export const PromptSection: FCVM<MainPageViewModel> = observer(({ vm }) => {
  return (
    <ScrollShadow className="flex flex-col gap-4 flex-1 overflow-auto bottom-inner-shadow pb-4">
      {vm.prompts.map((prompt, index) => (
        <PromptCard
          key={index}
          disabled={vm.isGenerating}
          prompt={prompt}
          onDelete={() => vm.removePrompt(index)}
        />
      ))}
      <div className="sticky bottom-0 z-10 min-h-[40px]">
        <Button
          isDisabled={vm.isGenerating}
          startContent={<PlusSvg className="w-6 h-6" />}
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
  return (
    <div className="flex items-center gap-1">
      <Button
        size="sm"
        isLoading={vm.isGenerating}
        onClick={() => vm.generate()}
        startContent={!vm.isGenerating && <WandSvg className="w-5 h-5" />}
        color="secondary">
        Начать генериацию
      </Button>
    </div>
  );
});
