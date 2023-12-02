import {
  Pattern,
  fetchImages,
  fetchPatterns,
  generateImage,
  generateImageByPattern
} from "api/endpoints/stickers.endpoint";
import { StickerDto } from "api/models/sticker.model";
import { makeAutoObservable } from "mobx";

export interface Prompt {
  positive: string;
  negative: string;
  count: number;
  isLoading?: boolean;
}

export interface Sticker {
  id: string;
  img?: string;
  isLoading?: boolean;
  prompt?: string;
  isSelected?: boolean;
}

const FETCH_INTERVAL = 10000;

export class MainPageViewModel {
  public prompts: Prompt[] = [
    {
      positive: "",
      negative: "",
      count: 2,
      isLoading: false
    }
  ];
  public favoriteStickers: Sticker[] = [];
  public generatedStickers: Sticker[] = [];
  public stickerPatterns: Record<string, Pattern> | null = null;
  public selectedPattern: Pattern | null = null;
  public isLoadingPattern = false;

  get stickers() {
    return [...this.favoriteStickers, ...this.generatedStickers];
  }

  constructor() {
    makeAutoObservable(this);
    this.init();
  }

  async init() {
    this.stickerPatterns = await fetchPatterns();
    const firstPattern = Object.keys(this.stickerPatterns)[0];
    this.selectedPattern = this.stickerPatterns[firstPattern];
  }

  async generateByPattern() {
    if (!this.selectedPattern) return;
    this.isLoadingPattern = true;
    try {
      const sticker = await generateImageByPattern(this.selectedPattern.title);
      this.generatedStickers.push({
        id: sticker.id,
        prompt: sticker.prompt,
        isLoading: true
      });

      const interval = setInterval(async () => {
        const images = await fetchImages([sticker.id]);
        const image = images[0];
        const index = this.generatedStickers.findIndex((s) => s.id === image.id);
        if (index === -1) return;
        this.generatedStickers[index].img = image.img;
        this.generatedStickers[index].isLoading = false;
        clearInterval(interval);
        this.isLoadingPattern = false;
      }, FETCH_INTERVAL);
    } catch {
      this.isLoadingPattern = false;
    }
  }

  addPrompt() {
    this.prompts.push({
      positive: "",
      negative: "",
      count: 2
    });
  }

  removePrompt(index: number) {
    this.prompts.splice(index, 1);
  }

  async generatePrompt(prompt: Prompt) {
    prompt.isLoading = true;
    try {
      const items = await Promise.all(
        Array.from({ length: prompt.count }).map(() =>
          generateImage({
            prompt: prompt.positive
          })
        )
      );

      items.forEach((item) =>
        this.generatedStickers.push({
          id: item.id,
          prompt: item.prompt,
          isLoading: true
        })
      );

      const interval = setInterval(async () => {
        const ids = items.map((s) => s.id);
        const images = await fetchImages(ids);

        images.forEach((image) => {
          const index = this.generatedStickers.findIndex((s) => s.id === image.id);
          if (index === -1) return;
          this.generatedStickers[index].img = image.img;
          this.generatedStickers[index].isLoading = false;
        });

        const isLoading = this.generatedStickers.some((s) => s.isLoading);
        if (!isLoading) {
          clearInterval(interval);
          prompt.isLoading = false;
        }
      }, FETCH_INTERVAL);
    } catch {
      prompt.isLoading = false;
    }
  }

  //#region dnd
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
      if (stickerToMove.isLoading) return;
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
    if (stickerToMove.isLoading) return;
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
  //#endregion
}
