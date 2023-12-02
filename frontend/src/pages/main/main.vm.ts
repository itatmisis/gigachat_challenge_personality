import { StickerDto } from "api/models/sticker.model";
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
  public favoriteStickers: StickerDto[] = [
    {
      id: "2"
    },
    {
      id: "3"
    }
  ];
  public generatedStickers: StickerDto[] = [
    {
      id: "1"
    },
    {
      id: "4"
    },
    {
      id: "5"
    },
    {
      id: "6"
    }
  ];

  get stickers() {
    return [...this.favoriteStickers, ...this.generatedStickers];
  }

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

  moveSticker(overId: string | null, fromId: string) {
    const isFromInFavorite = this.favoriteStickers.some((s) => s.id === fromId);
    let stickerToMove;

    if (isFromInFavorite) {
      const fromIndex = this.favoriteStickers.findIndex((s) => s.id === fromId);
      stickerToMove = this.favoriteStickers[fromIndex];
      this.favoriteStickers.splice(fromIndex, 1); // Remove sticker from favorites
    } else {
      const fromIndex = this.generatedStickers.findIndex((s) => s.id === fromId);
      stickerToMove = this.generatedStickers[fromIndex];
      this.generatedStickers.splice(fromIndex, 1); // Remove sticker from generated
    }

    if (stickerToMove) {
      const isOverInFavorite = this.favoriteStickers.some((s) => s.id === overId);

      if (isOverInFavorite) {
        const overIndex = this.favoriteStickers.findIndex((s) => s.id === overId);
        // Insert the sticker in the favorite list at the position of overId
        this.favoriteStickers.splice(overIndex, 0, stickerToMove);
      } else {
        const overIndex = this.generatedStickers.findIndex((s) => s.id === overId);
        // Insert the sticker in the generated list at the position of overId
        this.generatedStickers.splice(overIndex, 0, stickerToMove);
      }
    }
  }

  moveToFavorites(id: string) {
    const fromIndex = this.generatedStickers.findIndex((s) => s.id === id);
    if (fromIndex === -1) return;
    const stickerToMove = this.generatedStickers[fromIndex];
    this.generatedStickers.splice(fromIndex, 1); // Remove sticker from generated
    this.favoriteStickers.push(stickerToMove);
  }

  moveToGenerated(id: string) {
    const fromIndex = this.favoriteStickers.findIndex((s) => s.id === id);
    if (fromIndex === -1) return;
    const stickerToMove = this.favoriteStickers[fromIndex];
    this.favoriteStickers.splice(fromIndex, 1); // Remove sticker from favorites
    this.generatedStickers.push(stickerToMove);
  }
}
