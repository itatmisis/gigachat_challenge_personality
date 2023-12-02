import { makeAutoObservable } from "mobx";

export class LandingPageViewModel {
  constructor() {
    makeAutoObservable(this);
  }
}
