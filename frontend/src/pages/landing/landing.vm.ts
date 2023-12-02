import { makeAutoObservable } from "mobx";
import { Sticker } from "../main/main.vm";

export class LandingPageViewModel {
  public selectedStickers: Sticker[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  public addSticker(sticker: Sticker) {
    this.selectedStickers.push(sticker);
  }
}
