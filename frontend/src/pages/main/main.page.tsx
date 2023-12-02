import React, { useState } from "react";
import { GeneratedSection } from "./sections/generated.section";
import { observer } from "mobx-react-lite";
import { FavoritesSection } from "./sections/favorites.section";
import { PromptSection } from "./sections/prompt.section";
import { MainPageViewModel } from "../main.vm";
import cl from "./style.module.scss";

export const MainPage = observer(() => {
  const [vm] = useState(() => new MainPageViewModel());

  return (
  <main className={cl.layout}>
    <PromptSection vm={vm} />
    <GeneratedSection vm={vm} />
    <FavoritesSection vm={vm} />
  </main>
  );
});
