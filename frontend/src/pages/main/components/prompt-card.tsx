import { Card, CardBody, Textarea, Button, Tooltip } from "@nextui-org/react";
import { observer } from "mobx-react-lite";
import { Prompt } from "../main.vm";
import PlusSvg from "@/assets/icons/plus.svg";
import MinusSvg from "@/assets/icons/minus.svg";
import DeleteSvg from "@/assets/icons/delete.svg";
import WandSvg from "@/assets/icons/wand.svg";

export const PromptCard = observer(
  ({
    prompt,
    onDelete,
    onGenerate
  }: {
    prompt: Prompt;
    onDelete: () => void;
    onGenerate: () => void;
  }) => {
    const disabled = prompt.isLoading;

    return (
      <div className="flex gap-2 flex-1 items-center">
        <Card className="bg-default-100 flex-1" shadow="none">
          <CardBody>
            <div className="flex gap-2">
              <div className="flex flex-col gap-2 flex-1">
                <Textarea
                  isDisabled={disabled}
                  label="Тема стикеров"
                  variant="faded"
                  value={prompt.positive}
                  onChange={(e) => (prompt.positive = e.target.value)}
                />
                {/* <Input
                    isDisabled={disabled}
                    label="Негативный промпт"
                    variant="flat"
                    size="sm"
                    value={prompt.negative}
                    onChange={(e) => (prompt.negative = e.target.value)}
                  /> */}
              </div>
              <div className="flex flex-col items-center gap-1">
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
                <Tooltip showArrow content="Начать генерацию">
                  <Button
                    isLoading={prompt.isLoading}
                    isDisabled={disabled || prompt.positive.length === 0}
                    onClick={() => onGenerate()}
                    isIconOnly
                    color="secondary"
                    fullWidth
                    className="w-full"
                    variant="ghost">
                    <WandSvg className="w-5 h-5" />
                  </Button>
                </Tooltip>
              </div>
            </div>
            {/* <div className="flex items-center mt-3 mx-2"></div> */}
          </CardBody>
        </Card>
        <div className="flex flex-col gap-1">
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
      </div>
    );
  }
);
