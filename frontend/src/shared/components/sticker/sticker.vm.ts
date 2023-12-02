import { fetchImage } from "api/endpoints/stickers.endpoint";
import { makeAutoObservable } from "mobx";

export class StickerViewModel {
  public isLoading = true;
  public isSelected = false;
  public imgSrc: string | null = null;

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
    const imgSrc = await fetchImage(this.id);
    this.imgSrc = imgSrc;
    this.isLoading = false;
  }

  dispose() {}
}
