import { fetchImage } from "api/endpoints/stickers.endpoint";
import { makeAutoObservable } from "mobx";

export class StickerViewModel {
  constructor(
    public id: string,
    public img: string | null
  ) {
    makeAutoObservable(this);
    if (!img) {
      this.init();
    }
  }

  async init() {
    const img = await fetchImage(this.id);
    this.img = img as string;
  }

  dispose() {}
}
