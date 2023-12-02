import { fetchImage } from "api/endpoints/stickers.endpoint";
import { makeAutoObservable } from "mobx";

export class StickerViewModel {
  public isLoading = true;
  public isSelected = false;

  constructor(
    public id: string,
    public img: string | null
  ) {
    makeAutoObservable(this);
    if (img) {
      this.isLoading = false;
    } else {
      this.init();
    }
  }

  async init() {
    const img = await fetchImage(this.id);
    this.img = img as string;
  }

  dispose() {}
}
