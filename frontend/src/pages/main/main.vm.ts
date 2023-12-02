import { makeAutoObservable } from "mobx";

export interface Prompt {
  positive: string;
  negative: string;
  count: number;
}

export class MainPageViewModel {
  public prompts: Prompt[] = [
    {
      positive: "",
      negative: "",
      count: 4
    }
  ];
  public isGenerating = false;

  constructor() {
    makeAutoObservable(this);
  }

  addPrompt() {
    this.prompts.push({
      positive: "",
      negative: "",
      count: 4
    });
  }

  removePrompt(index: number) {
    this.prompts.splice(index, 1);
  }

  async generate() {
    this.isGenerating = true;
    await new Promise((resolve) => setTimeout(resolve, 1000));
    this.isGenerating = false;
  }

  dispose() {}
}
