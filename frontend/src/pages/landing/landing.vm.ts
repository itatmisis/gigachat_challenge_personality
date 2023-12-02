import { makeAutoObservable } from "mobx";
import { Sticker } from "../main/main.vm";
import { fetchAll } from "api/endpoints/stickers.endpoint";
import { StickerViewModel } from "@/components/sticker/sticker.vm";

export class LandingPageViewModel {
  public selectedStickers: StickerViewModel[] = [];
  public images: StickerViewModel[] = [];
  public otherImages: Record<string, StickerViewModel[]> = {};

  constructor() {
    makeAutoObservable(this);
    this.init();
  }

  public async init() {
    const res = await fetchAll();

    const random = res.images.random;
    if (random) {
      random.map((v) => {
        this.images.push(new StickerViewModel(v.id, v.img));
      });
    }

    const keys = Object.keys(res.images);
    keys.splice(keys.indexOf("random"), 1);
    keys.map((key) => {
      const arr = res.images[key];
      this.otherImages[key] = arr.map((v) => {
        return new StickerViewModel(v.id, v.img);
      });
    });
  }

  public addSticker(sticker: StickerViewModel) {
    if (sticker.isSelected) {
      sticker.isSelected = false;
      this.selectedStickers.splice(this.selectedStickers.indexOf(sticker), 1);
      return;
    }
    sticker.isSelected = true;
    this.selectedStickers.push(sticker);
  }

  public navigateConstructor() {
    const ids = this.selectedStickers.map((v) => v.id);
    window.location.href = `/constructor?ids=${ids.join(",")}`;
  }
}
