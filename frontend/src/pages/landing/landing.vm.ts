import { makeAutoObservable } from "mobx";
import { Sticker } from "../main/main.vm";
import { fetchAll } from "api/endpoints/stickers.endpoint";
import { StickerViewModel } from "@/components/sticker/sticker.vm";

export class LandingPageViewModel {
  public selectedStickers: Sticker[] = [];
  public images: StickerViewModel[] = [];

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
  }

  public addSticker(sticker: Sticker) {
    this.selectedStickers.push(sticker);
  }
}
